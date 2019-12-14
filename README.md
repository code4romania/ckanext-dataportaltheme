ckanext-dataportaltheme
=============

DataPortal base theme

[UI prototype](https://www.figma.com/file/P60qSupJkefpT7K4rT5PQuva/Data-Portal?node-id=0%3A1)


## Requirements


To start working on this extension you will need [Virtualbox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/)

We gave 4096MB of RAM to the VM. If you wish you can change this in the `Vagrantfile`


## Start Virtual Machine

```
./bin/start.sh
```
Take a break for 10-15 min :).  

If you have errors in during start, please check that you have the latest [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/), or try to run step by step the commands from [Installing CKAN from source](https://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html) documentation

Now you can access ckan instance on http://127.0.0.1:5000

You have 4 available users:
```
admin (password: "changeme") - sysadmin
demo (password: "changeme") - admin user in Code4 Organisation
editor (password: "changeme") - editor user in Code4 Organisation
member (password: "changeme") - regular user(member) in Code4 Organisation
```

# Happy Hacking :)

## Translating content
All texts in the templates or controllers should be written in english using i18n tags.  
If you added a new string or block you need to run (from `/vagrant`, with the virtualenv activated):
```
python setup.py extract_messages
python setup.py update_catalog --locale ro -d  ckanext/dataportaltheme/i18n/
python setup.py update_catalog --locale hu -d  ckanext/dataportaltheme/i18n/
```

After you modify the `.po` file for each language, run this command:
```
python setup.py compile_catalog --locale ro -d ckanext/dataportaltheme/i18n/
```



## Restore the database

```
paster --plugin=ckan db clean -c /etc/ckan/default/development.ini
sudo -u postgres pg_restore --clean --if-exists -d ckan_default < /data/ckan.dump
```

### CKAN Documentation
[CKAN Docs](https://docs.ckan.org/en/2.8/)  
[CKAN Extensions Tutorial](https://docs.ckan.org/en/2.8/extensions/tutorial.html)  
[CKAN Theming guide](https://docs.ckan.org/en/2.8/theming/)

### Resources
[Add static pages extension example](https://github.com/okfn/ckanext-sa/blob/master/ckanext/sa/plugin.py)
[Base template](https://github.com/ckan/ckan/tree/master/ckan/templates)


# Contributing 

If you would like to contribute to one of our repositories, first identify the scale of what you would like to contribute. If it is small (grammar/spelling or a bug fix) feel free to start working on a fix. If you are submitting a feature or substantial code contribution, please discuss it with the team and ensure it follows the product roadmap. 

Our collaboration model [is described here](WORKFLOW.md).


