# pg_monitor
Postgres Cluster Monitor using repmgr. Python replacement for repmgrd

A quick a dirty python replacement for repmgrd which wouldn't cordinate reliably a replication
failover. When the master fails, this monitor will promote the slave to master.

Run this monitor on the slave. When the master fails the script will promote the slave to the master.



