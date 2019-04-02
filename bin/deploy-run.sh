#!/bin/bash

sudo service apache2 stop
sudo service nginx stop

sudo service apache2 status
sudo service nginx status

. /usr/lib/ckan/default/bin/activate

sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-dataportaltheme.git#egg=ckanext-dataportaltheme
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-mediumfeed.git#egg=ckanext-mediumfeed
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-githubfeed.git#egg=ckanext-githubfeed

sudo service apache2 start
sudo service nginx start