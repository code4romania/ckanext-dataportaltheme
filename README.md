ckanext-dataportaltheme
=============

DataPortal base theme


------------
Requirements
------------

To start working on this extension you will need [Virtualbox](https://www.virtualbox.org/) and [Vagrant] (https://www.vagrantup.com/)

-------------
Start Vagrant
-------------
```
vagrant up
vagrant ssh
```
If you get any error while `vagrant up` try `vagrant reload`

------------------------------------------
Activate virtualenv and install the plugin
------------------------------------------
```
source /usr/lib/ckan/default/bin/activate
cd /vagrant
sudo python setup.py develop
```

-----------------------------
Start CKAN development server
-----------------------------
Before starting the development server be sure to set  `debug=true`, and add `dataportaltheme` in `ckan.plugins` in `/vagrant/ckan/development.ini`
```
sudo paster serve /vagrant/ckan/development.ini --reload
```

-----------------
Create admin user
-----------------
```
paster --plugin=ckan sysadmin add admin -c /vagrant/ckan/development.ini
```


# CKAN Documentation
[CKAN Docs](https://docs.ckan.org/en/2.8/)
[CKAN Extensions Tutorial](https://docs.ckan.org/en/2.8/extensions/tutorial.html)



------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-dataportaltheme:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-dataportaltheme Python package into your virtual environment::

     pip install ckanext-dataportaltheme

3. Add ``dataportaltheme`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.dataportaltheme.some_setting = some_default_value


------------------------
Development Installation
------------------------

To install ckanext-dataportaltheme for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/code4romania/ckanext-dataportaltheme.git
    cd ckanext-dataportaltheme
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.dataportaltheme --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-dataportaltheme on PyPI
---------------------------------

ckanext-dataportaltheme should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-dataportaltheme. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-dataportaltheme
----------------------------------------

ckanext-dataportaltheme is availabe on PyPI as https://pypi.python.org/pypi/ckanext-dataportaltheme.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
