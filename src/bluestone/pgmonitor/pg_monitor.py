#!/usr/bin/env python

"""
Script to monitor the master and slave nodes and automate the promotion of the slave should the master fail.
"""

import imp
from sqlalchemy import *
import sqlalchemy.exc
import time
import datetime
import subprocess

import argparse


def import_config( name, filepath):
  d = imp.new_module( name )
  d.__file__ = filepath

  cfgmap = {}
  try:
    with open(filepath) as cfg_file:
      exec( compile( cfg_file.read(), filepath, 'exec'), cfgmap )
  except IOError as e:
    e.strerror = 'Unable to load config file (%s)' % e.strerror
    raise
  return cfgmap

def isempty(str):
    return not( str and str.strip() != "" )

class MasterFailed(Exception):
    pass

class ValidateRepmgr(object):

    def validate(self, repmgr):
        """Check for the values we need to successfully monitor the cluster"""

        assert repmgr.get( 'promote_command' )
        assert repmgr.get( 'reconnect_attempts' )
        assert repmgr.get( 'reconnect_interval' )
        assert repmgr.get( 'cluster' )
        assert repmgr.get( 'node' )
        assert repmgr.get( 'node_name' )
        assert repmgr.get( 'failover' )
        assert repmgr.get( 'master_response_timeout' )        
        
        

class PgClusterMonitor(object):

    def __init__(self, configfile, quiet=False):
        self.configfile = configfile
        self.config = self.loadConfig( configfile )
        self.quiet = quiet
      
        self.pgnodes = self.config['PG_NODES']

        for node in self.pgnodes:
            name = node.get( "name" , None )
            if name:
                node[ 'conninfo' ]  = self.config['PG_CONN_INFO'].get( name, None )

        self.loadReprMgr( self.config[ 'REPMGR_CONFIG' ] )

        self.cluster = self.repmgr[ 'cluster' ]
        self.failover = self.repmgr.get( 'failover', 'manual' )
        self.promote_command = self.repmgr[ 'promote_command' ]
        self.reconnect_attempts = self.repmgr[ 'reconnect_attempts' ]
        self.reconnect_interval = self.repmgr[ 'reconnect_interval' ]


    def loadConfig(self, configfile ):
      try:
        cfg = import_config( "config", configfile )
        assert cfg['PG_NODES']
        assert cfg['PG_CONN_INFO']
        assert cfg['REPMGR_CONFIG']
      except:
        print( """configfile must be specified and reference a valid configuration file. 
A valid configuration is a python file (with any extension) with the following parameters set:

# An enumeration of all nodes in the cluster
PG_NODES = [ { 'name': 'pgnode1', 'type': 'master' }, {'name': 'pgnode2', 'type': 'slave'} ]
# A dictionary of connect strings for every node in the cluster
PG_CONN_INFO = { 'pgnode1' : 'postgresql://user:password@pgnode1.host.com:5432/dbname' }
# The location of repmgr.conf file for the node. This is the same file you pass to repmgr commands
REPR_CONFIG = "/var/lib/postgresql/repmgr/repmgr.conf"

""" )
        raise

      return cfg
        
    def loadReprMgr(self, repmgrconf):
        self.repmgr = import_config( "repmgr", repmgrconf )
        v = ValidateRepmgr()
        v.validate( self.repmgr )        

        
    def monitor(self):

        # Monitor until a failure event occurs.
        failure=False

        while not( failure ):
            try:
                enginemap = self.check_nodes()

                if not(self.quiet):
                  print("[%s] Cluster %s is healthy." % (datetime.datetime.now(), self.cluster) )
                time.sleep(15)
            except:
                failure = True
                raise


    def check_nodes(self):
        enginemap = {}
        for n in self.pgnodes:
            conn = self.check_node(n)
            enginemap[ n.get('name')] = n

            if not(conn) and n.get('type') == 'master':
                print( "[%s] master failed" % datetime.datetime.now() )
                self.promote_slave()
                
                raise MasterFailed( "Master failed" )

            conn.close()

        return enginemap

    def _promote_slave(self):
        print( "%s" % self.promote_command )
        proc = subprocess.Popen( self.promote_command, shell=True, stdout=subprocess.PIPE )

        pstdout = proc.communicate()[0]

        print( repr(pstdout) )
        return True

        

    def promote_slave(self):
        for n in self.pgnodes:
            if n['type'] == 'slave':
                conn = self.check_node( n )

                if conn:
                    print( "[%s] Slave %s is up. Attempting to promote it." % (datetime.datetime.now(), n['name']) )
                    self._promote_slave()
                    conn.close()
                    
                
    def check_node(self, node):
        conn = None
        reconnect_attempts = self.reconnect_attempts
        err = None

        while reconnect_attempts>0 and not(conn):
            try:
                engine = node.get( 'engine' , None )
                if not(engine):
                  engine = create_engine( node.get( 'conninfo' ) )
                  node[ 'engine' ] = engine

                conn = engine.connect()
                res = conn.execute( 'SELECT current_timestamp' )
                res.close()
                err = None
            except Exception as e :
                reconnect_attempts=reconnect_attempts-1
                time.sleep( self.reconnect_interval )
                conn = None
                
                err = e
                
        if err:
            import traceback
            print( err )
            traceback.print_exc( err )
        
        return conn
        

def main():
    ap = argparse.ArgumentParser(description='Bluestone PG Monitor Tool.')
    ap.add_argument('-q','--quiet', help='Reduce the verbosity of the tool.', default="false")
    ap.add_argument('-c','--configfile', help='Specify the location of the config file.', default='pg_monitor.conf')

    args = ap.parse_args()

    quiet = True if args.quiet == "true" else False
  
  
    mon = PgClusterMonitor(args.configfile, quiet=quiet)
    mon.monitor()
    
    
if __name__ == '__main__':
    main()
