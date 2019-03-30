#!/bin/bash

PASTER_PID="$(ps -a | grep paster | awk {'print $1'})"
PYTHON_PID="$(sudo lsof -i :5000 | awk 'NR>1 {print $2}')"

if [ "$PASTER_PID" ]; then
        echo "Stopping process with PID $PASTER_PID"
        sudo kill -9 $PASTER_PID
else
	echo "No paster process found"
fi

if [ "$PYTHON_PID" ]; then
        echo "Stopping process with PID $PYTHON_PID"
        sudo kill -9 $PYTHON_PID
else
	echo "No process running on port 5000 found"
fi

. /usr/lib/ckan/default/bin/activate

sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-dataportaltheme.git#egg=ckanext-dataportaltheme
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-mediumfeed.git#egg=ckanext-mediumfeed
sudo /usr/lib/ckan/default/bin/pip install -e git+https://github.com/code4romania/ckanext-githubfeed.git#egg=ckanext-githubfeed

sudo /usr/lib/ckan/default/bin/paster serve /home/deploy/config/development.ini --reload &