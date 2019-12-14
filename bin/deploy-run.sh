#!/bin/bash

. /usr/lib/ckan/default/bin/activate

sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-dataportaltheme.git#egg=ckanext-dataportaltheme
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-mediumfeed.git#egg=ckanext-mediumfeed
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-githubfeed.git#egg=ckanext-githubfeed
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/OpenGov-OpenData/ckanext-odata#egg=ckanext-odata
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/geosolutions-it/ckanext-tableauview.git#egg=ckanext-tableauview
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/costibleotu/ckanext-datarequests#egg=ckanext-datarequests

sudo service apache2 reload
sudo service nginx reload