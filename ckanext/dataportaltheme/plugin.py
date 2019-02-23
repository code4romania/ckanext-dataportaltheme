import routes.mapper
import ckan.lib.base as base
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from datetime import datetime

import requests
import json

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


class DataportalthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
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
        return route_map

    def after_map(self, route_map):
        return route_map

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'all_groups': all_groups,
            'current_year': datetime.now().year,
            'githubfeed_gettasks': gettasks,
            'githubfeed_getallissuesurl': toolkit.config.get('ckan.githubfeed.allissuesurl', 
                    'https://github.com/orgs/code4romania/projects/12')
        }

class PortalController(base.BaseController):
    def dataStatsEsentiale(self):
        return base.render('dataStas/esentiale.html')

    def dataStatsStruct(self):
        return base.render('dataStas/struct.html')
