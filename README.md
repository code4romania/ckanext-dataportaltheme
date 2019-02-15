ckanext-dataportaltheme
=============

DataPortal base theme

[UI prototipe](https://www.figma.com/file/P60qSupJkefpT7K4rT5PQuva/Data-Portal?node-id=0%3A1)

------------
Requirements
------------

To start working on this extension you will need [Virtualbox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/)

We gave 4096MB of RAM to the VM. If you wish you can change this in the `Vagrantfile`

---------------------
Start Virtual Machine
---------------------
```
vagrant up
vagrant ssh
```
Take a break for 10-15 min :).  
If you get any error while `vagrant up` try `vagrant reload`.  

If you still have errors in during `vagrant up` please check that you have the latest `Vagrant` and `Virtualbox`, or try to run step by step the commands from [Installing CKAN from source](https://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html) documentation

------------------------------------------
Activate virtualenv
------------------------------------------
```
source /usr/lib/ckan/default/bin/activate
```


-----------------------------
Start CKAN development server
-----------------------------
```
paster serve /etc/ckan/default/development.ini --reload
```


Now you can access ckan instance on http://127.0.0.1:5000

You have 4 available users:
```
admin (pasword: "changeme") - sysadmin
demo (pasword: "changeme") - admin user in Code4 Organization
editor (pasword: "changeme") - editor user in Code4 Organization
member (pasword: "changeme") - regular user(member) in Code4 Organization
```

# Happy Hacking :)

-----------------
Restore the database
-----------------
```
paster --plugin=ckan db clean -c /etc/ckan/default/development.ini
sudo -u postgres pg_restore --clean --if-exists -d ckan_default < /data/ckan.dump
```

# CKAN Documentation
[CKAN Docs](https://docs.ckan.org/en/2.8/)  
[CKAN Extensions Tutorial](https://docs.ckan.org/en/2.8/extensions/tutorial.html)  
[CKAN Theming guide](https://docs.ckan.org/en/2.8/theming/)

# Resources
[Add static pages extension example](https://github.com/okfn/ckanext-sa/blob/master/ckanext/sa/plugin.py)

---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.dataportaltheme.some_setting = some_default_value


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
