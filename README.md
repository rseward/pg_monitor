# pg_monitor
Postgres Cluster Monitor using repmgr. Python replacement for repmgrd

A quick a dirty python replacement for repmgrd which wouldn't cordinate reliably a replication
failover. When the master fails, this monitor will promote the slave to master.

Run this monitor on the slave. When the master fails the script will promote the slave to the master.

# Quick Install

    sudo -i
    yum install python-virtualenv

    su postgresql -
    cd $HOME
    mkdir -p ~/pyve/
    virtualenv ~/pyve/
    source ~/pyve/bin/activate
    
    git clone https://githib.com/rseward/pg_monitor.git
    cd pg_monitor
    export PATH="$PATH:/usr/pgsql-9.4/bin/"
    pip install -r requirements.txt
    ./install.sh

    cp samples/pgmon.conf.sample /var/lib/postgresql/repmgr/pgmon.conf
		edit /var/lib/postgresql/repmgr/pgmon.conf
		



