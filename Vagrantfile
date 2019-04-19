# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/xenial64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8800, host: 8800
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.synced_folder "etc/", "/etc/ckan/default"
  config.vm.synced_folder "data/", "/data"
  # config.vm.synced_folder "src/", "/usr/lib/ckan/default/src"
  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
    vb.memory = "4096"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python-dev postgresql libpq-dev python-pip python-virtualenv git-core solr-jetty openjdk-8-jdk redis-server build-essential libxslt1-dev libxml2-dev git libffi-dev apache2 libapache2-mod-wsgi supervisor postgresql-9.5-postgis-2.2

    mkdir -p /home/vagrant/ckan/lib
    sudo ln -s /home/vagrant/ckan/lib /usr/lib/ckan
    mkdir -p /home/vagrant/ckan/etc
    sudo ln -s /home/vagrant/ckan/etc /etc/ckan
    sudo mkdir -p /usr/lib/ckan/default
    sudo chown `whoami` /usr/lib/ckan/default
    sudo mkdir -p /var/lib/ckan/storage
    # sudo mkdir -p /var/lib/ckan/resources
    cp -r /data/storage/* /var/lib/ckan/storage
    # sudo cp -r /data/resources/* /var/lib/ckan/resources
    sudo chown -R vagrant:vagrant /var/lib/ckan
    sudo chown -R vagrant:vagrant /usr/lib/ckan
    virtualenv --no-site-packages /usr/lib/ckan/default
    virtualenv --no-site-packages /usr/lib/ckan/datapusher
    . /usr/lib/ckan/default/bin/activate
    pip install setuptools==36.1
    pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.8.2#egg=ckan'
    pip install -e 'git+https://github.com/ViderumGlobal/ckanext-c3charts#egg=ckanext-c3charts'
    pip install -e "git+https://github.com/ckan/ckanext-spatial.git#egg=ckanext-spatial"
    pip install -r /usr/lib/ckan/default/src/ckanext-spatial/pip-requirements.txt
    pip install -e 'git+https://github.com/ckan/ckanext-geoview#egg=ckanext-geoview'
    pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt
    pip install flask_debugtoolbar ckantoolkit ckanext-geoview
    cd /vagrant
    python setup.py develop
    deactivate
    . /usr/lib/ckan/default/bin/activate
    sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'ckan_default';"
    sudo -u postgres psql -c "CREATE USER datastore_default WITH PASSWORD 'ckan_default';"
    sudo -u postgres createdb -O ckan_default ckan_default -E utf-8
    sudo -u postgres createdb -O ckan_default datastore_default -E utf-8
    sudo -u postgres createdb -O ckan_default xloader_jobs -E utf-8
    sudo -u postgres psql -c "GRANT ALL ON DATABASE ckan_default TO ckan_default;"
    sudo -u postgres psql -c "GRANT ALL ON DATABASE xloader_jobs TO ckan_default;"
    sudo -u postgres psql -c "GRANT ALL ON DATABASE datastore_default TO ckan_default;"
    sudo -u postgres psql -d ckan_default -f /usr/share/postgresql/9.5/contrib/postgis-2.2/postgis.sql
    sudo -u postgres psql -d ckan_default -f /usr/share/postgresql/9.5/contrib/postgis-2.2/spatial_ref_sys.sql
    sudo -u postgres psql -d ckan_default -c 'ALTER VIEW geometry_columns OWNER TO ckan_default;'
    sudo -u postgres psql -d ckan_default -c 'ALTER TABLE spatial_ref_sys OWNER TO ckan_default;'
    cd /tmp
    git clone https://github.com/ckan/ckanext-xloader
    cd ckanext-xloader
    sudo -u postgres psql datastore_default -f /tmp/ckanext-xloader/full_text_function.sql
    pip install ckanext-xloader
    pip install -r requirements.txt
    pip install -U requests[security]
    pip install -U cachetools
    sudo -u postgres psql datastore_default -f /tmp/ckanext-xloader/full_text_function.sql
    cp /etc/ckan/default/pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf
    sudo service postgresql restart
    cp /etc/ckan/default/jetty8 /etc/default/jetty
    sudo service jetty8 restart
    sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
    sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
    sudo service jetty8 restart
    cd /usr/lib/ckan/default/src/ckan
    paster db clean -c /etc/ckan/default/development.ini
    # sudo -u postgres psql postgres ckan_default  < /data/ckan_default.dump 
    # sudo -u postgres psql postgres datastore_default  < /data/datastore_default.dump 
    # sudo -u postgres psql postgres xloader_jobs  < /data/xloader_jobs.dump 
    sudo -u postgres pg_restore --clean --if-exists -d ckan_default  < /data/ckan_default.dump 
    sudo -u postgres pg_restore --clean --if-exists -d datastore_default  < /data/datastore_default.dump 
    sudo -u postgres pg_restore --clean --if-exists -d xloader_jobs  < /data/xloader_jobs.dump 
    paster --plugin=ckan search-index rebuild --config=/etc/ckan/default/development.ini
    paster --plugin=ckan datastore set-permissions -c /etc/ckan/default/development.ini | sudo -u postgres psql ckan_default --set ON_ERROR_STOP=1
    deactivate
    sudo chown -R vagrant:vagrant /var/lib/ckan/
    sudo chown -R vagrant:vagrant /usr/lib/ckan/
    sudo cp /etc/ckan/default/supervisor/xloader.conf /etc/supervisor/conf.d
    sudo service supervisor restart

    # . /usr/lib/ckan/datapusher/bin/activate

    # mkdir /usr/lib/ckan/datapusher/src
    # cd /usr/lib/ckan/datapusher/src

    # git clone -b 0.0.14 https://github.com/ckan/datapusher.git

    # cd datapusher
    # pip install -r requirements.txt
    # python setup.py develop


    # sudo cp deployment/datapusher.apache2-4.conf /etc/apache2/sites-available/datapusher.conf
    # sudo cp deployment/datapusher.wsgi /etc/ckan/

    # # #copy the standard DataPusher settings.
    # sudo cp deployment/datapusher_settings.py /etc/ckan/

    
    # sudo sh -c 'echo "NameVirtualHost *:8800" >> /etc/apache2/ports.conf'
    # sudo sh -c 'echo "Listen 8800" >> /etc/apache2/ports.conf'
    # echo "ServerName localhost" | sudo tee /etc/apache2/conf-available/fqdn.conf
    # sudo a2enconf fqdn

    # sudo chown -R vagrant:vagrant /var/lib/ckan/
    # sudo chown -R vagrant:vagrant /usr/lib/ckan/
    # sudo a2ensite datapusher
    # sudo service apache2 reload
  SHELL
end
