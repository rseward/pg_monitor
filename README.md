# pg_monitor
Postgres Cluster Monitor using repmgr. Python replacement for repmgrd

This tool is a supplement to these instructions for a complete automated Postgres failover recipe. https://github.com/rseward/pg-failover-repmgr/

A quick a dirty python replacement for repmgrd. I found repmgrd buggy and un-reliable for cordinating replication
failovers. When the master fails, this python monitor will promote the slave to master and send an e-mail notification.

Run this monitor on the slave with the postgres UNIX user. When the master fails the script will promote the slave to the master.

# Install Pre-requirements

## Install Postgres Database Group Repo to install the required PGDG rpms.

    yum -y localinstall http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-1.noarch.rpm
    yum -y install postgresql94-server postgresql94-devel
    yum install -y http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/repmgr94-3.0.2-1.rhel7.x86_64.rpm
    # or yum install -y http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/repmgr94-3.0.2-1.rhel6.x86_64.rpm

# Quick Install

    sudo -i
    yum install python-virtualenv

    grep postgres /etc/passwd  # to find the home directory for your postgres directory
		# on my Centos and Fedora machines this is /var/lib/postgresql/. If it differs on
		# your machine make sure to substitute your home dir location in all configuration.

    su postgres -
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
    
    # Install init.d script to conveniently start and stop the monitor
    $( which deploy-pgmon-init-scripts )
		
    # Switch back to the root user
		cd generated-init-script
		./runasroot.sh  # Create the init script with the generated runasroot.sh script
    chkconfig --add pgmonitor
    chkconfig --list pgmonitor
    
    /etc/init.d/pgmonitor start

# Additional Notes.

To be documented.

