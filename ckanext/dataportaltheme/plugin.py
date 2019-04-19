import routes.mapper
import ckan.lib.base as base
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers
from datetime import datetime

import requests
import json
from cachetools.func import ttl_cache
from pprint import pprint

@ttl_cache(ttl=60 * 60)
def gettasks(params = {'state': 'open'}):
    url = toolkit.config.get('ckan.githubfeed.requesturl',
        'https://api.github.com/repos/code4romania/ckanext-dataportaltheme/issues')
    r = requests.get(url=url, params=params)
    obj = json.loads(r.text)
    return obj


def all_groups():
    '''Return a sorted list of the groups with the most datasets.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={'all_fields': True})

    return groups


def similar_with(current_package):
    if len(current_package['groups']) == 0:
        return []

    group = current_package['groups'][0]['name']
    
    f_group_packages = toolkit.get_action('group_package_show')
    packages = f_group_packages(data_dict={'id': group, 'limit': 3})

    # Delete current package from list if present
    idx_to_remove = -1
    for idx, package in enumerate(packages):
        if package['name'] == current_package['name']:
            idx_to_remove = idx
            break
    if idx_to_remove != -1:
        packages.pop(idx_to_remove)

    return packages

def generate_url(package):
    site_url = toolkit.config.get('ckan.site_url')
    relative_path = helpers.url_for_static(controller='package', action='read',id=package['name'])
    return ''.join([site_url, relative_path])

class DataportalthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    # plugins.implements(plugins.IResourceController)
    # IConfigurer

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        toolkit.add_resource('fanstatic', 'dataportaltheme')
        toolkit.add_resource('fanstatic', 'githubfeed')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

    def before_map(self, route_map):
        with routes.mapper.SubMapper(route_map, controller='ckanext.dataportaltheme.plugin:PortalController') as map:
            map.connect('stas-date-esentiale', '/standard-date/esentiale', action='dataStatsEsentiale')
            map.connect('stas-date-struct', '/standard-date/structura', action='dataStatsStruct')
            map.connect('terms-and-conditions', '/termsandconditions', action='termsandconditions')
            map.connect('code-of-conduct', '/codeofconduct', action='codeOfConduct')
        return route_map

    def after_map(self, route_map):
        return route_map

    def before_show(self, resource_dict):
        resource_dict['test'] = 'test'
        return resource_dict

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Catch github API limit exception
        try:
            latest_issues = gettasks()[:3]
        except:
            latest_issues = []
        return {
            'all_groups': all_groups,
            'current_year': datetime.now().year,
            'githubfeed_latest': latest_issues,
            'githubfeed_getallissuesurl': toolkit.config.get('ckan.githubfeed.allissuesurl', 
                    'https://github.com/orgs/code4romania/projects/12'),
            'similar': similar_with,
            'generate_url': generate_url
        }

class PortalController(base.BaseController):
    def dataStatsEsentiale(self):
        return base.render('dataStas/esentiale.html')

    def dataStatsStruct(self):
        return base.render('dataStas/struct.html')

    def termsandconditions(self):
        return base.render('home/termsandconditions.html')

    def codeOfConduct(self):
        return base.render('home/codeofconduct.html')