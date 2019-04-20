import routes.mapper
import ckan.lib.base as base
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.common import config
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
from ckan.controllers.home import CACHE_PARAMETERS

from datetime import datetime

import requests
import json
from cachetools.func import ttl_cache
from pprint import pprint


c = base.c
request = base.request

@ttl_cache(ttl=60 * 60)
def gettasks(params={'state': 'open'}):
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
    relative_path = h.url_for_static(
        controller='package', action='read', id=package['name'])
    return ''.join([site_url, relative_path])


class DataportalthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # plugins.implements(plugins.IResourceController)

    def update_config_schema(self, schema):

        ignore_missing = toolkit.get_validator('ignore_missing')

        schema.update({
            # This is an existing CKAN core configuration option, we are just
            # making it available to be editable at runtime
            'partner1_link': [ignore_missing],
            'partner1_logo': [ignore_missing],
            'partner2_link': [ignore_missing],
            'partner2_logo': [ignore_missing],
            'partner3_link': [ignore_missing],
            'partner3_logo': [ignore_missing],
            'partner4_link': [ignore_missing],
            'partner4_logo': [ignore_missing],
            'partner5_link': [ignore_missing],
            'partner5_logo': [ignore_missing],
            'partner6_link': [ignore_missing],
            'partner6_logo': [ignore_missing],
            'partner7_link': [ignore_missing],
            'partner7_logo': [ignore_missing],
            'partner8_link': [ignore_missing],
            'partner8_logo': [ignore_missing],
            'facebook_url': [ignore_missing],
            'twitter_url': [ignore_missing],
            'instagram_url': [ignore_missing],
            'linkedIn_url': [ignore_missing],
        })

        return schema

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
            map.connect('stas-date-esentiale',
                        '/standard-date/esentiale', action='dataStatsEsentiale')
            map.connect('stas-date-struct',
                        '/standard-date/structura', action='dataStatsStruct')
            map.connect('terms-and-conditions',
                        '/termsandconditions', action='termsandconditions')
            map.connect('contact-form', '/contact-form', action='contactForm')
            map.connect('cookie-policy', '/cookiepolicy',
                        action='cookiePolicy')
            map.connect('code-of-conduct', '/codeofconduct',
                        action='codeOfConduct')
            map.connect('admin.dataportal', '/ckan-admin/dataportal', action='dataportalAdmin')
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
            'generate_url': generate_url,
        }


class PortalController(base.BaseController):

    def _get_config_form_items(self):
        # Styles for use in the form.select() macro.
        styles = [{'text': 'Default', 'value': '/base/css/main.css'},
                  {'text': 'Red', 'value': '/base/css/red.css'},
                  {'text': 'Green', 'value': '/base/css/green.css'},
                  {'text': 'Maroon', 'value': '/base/css/maroon.css'},
                  {'text': 'Fuchsia', 'value': '/base/css/fuchsia.css'}]

        homepages = [{'value': '1', 'text': 'Introductory area, search, featured group and featured organization'},
                     {'value': '2', 'text': 'Search, stats, introductory area, featured organization and featured group'},
                     {'value': '3', 'text': 'Search, introductory area and stats'}]

        items = [
            {'name': 'ckan.site_title', 'control': 'input', 'label': _('Site Title'), 'placeholder': ''},
            {'name': 'ckan.main_css', 'control': 'select', 'options': styles, 'label': _('Style'), 'placeholder': ''},
            {'name': 'ckan.site_description', 'control': 'input', 'label': _('Site Tag Line'), 'placeholder': ''},
            {'name': 'ckan.site_logo', 'control': 'image_upload', 'label': _('Site Tag Logo'), 'placeholder': '', 'upload_enabled':h.uploads_enabled(),
                'field_url': 'ckan.site_logo', 'field_upload': 'logo_upload', 'field_clear': 'clear_logo_upload'},
            {'name': 'ckan.site_about', 'control': 'markdown', 'label': _('About'), 'placeholder': _('About page text')},
            {'name': 'ckan.site_intro_text', 'control': 'markdown', 'label': _('Intro Text'), 'placeholder': _('Text on home page')},
            {'name': 'ckan.site_custom_css', 'control': 'textarea', 'label': _('Custom CSS'), 'placeholder': _('Customisable css inserted into the page header')},
            {'name': 'ckan.homepage_style', 'control': 'select', 'options': homepages, 'label': _('Homepage'), 'placeholder': ''},
        ]
        return items

    def dataStatsEsentiale(self):
        return base.render('dataStas/esentiale.html')

    def dataStatsStruct(self):
        return base.render('dataStas/struct.html')

    def termsandconditions(self):
        return base.render('home/termsandconditions.html')

    def contactForm(self):
        request_params = plugins.toolkit.request.params
        url = 'https://docs.google.com/forms/u/2/d/e/1FAIpQLSeGNW5FjBwauZLsf0Ar8P6SgbTdd0n5hRfCAJ-XKtzWQMSqRA/formResponse'
        form_data = {'entry.268426185': request_params['email'],
                     'entry.782078158': request_params['message'],
                     'draftResponse': [],
                     'fvv': 1,
                     'pageHistory': 0}
        user_agent = {'Referer': 'https://docs.google.com/forms/d/e/1FAIpQLSeGNW5FjBwauZLsf0Ar8P6SgbTdd0n5hRfCAJ-XKtzWQMSqRA/viewform',
                      'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
        r = requests.post(url, data=form_data, headers=user_agent)
        return base.render('home/contactform.html')

    def cookiePolicy(self):
        return base.render('home/cookiepolicy.html')

    def codeOfConduct(self):
        return base.render('home/codeofconduct.html')

    def dataportalAdmin(self):
        # items = self._get_config_form_items()
        data = request.POST
        if 'save' in data:
            try:
                # really?
                data_dict = logic.clean_dict(
                    dict_fns.unflatten(
                        logic.tuplize_dict(
                            logic.parse_params(
                                request.POST, ignore_keys=CACHE_PARAMETERS))))
                pprint(data_dict)
                del data_dict['save']

                data = logic.get_action('config_option_update')(
                    {'user': c.user}, data_dict)
            except logic.ValidationError as e:
                errors = e.error_dict
                error_summary = e.error_summary
                vars = {'data': data, 'errors': errors,
                        'error_summary': error_summary}
                return base.render('admin/dataportal.html', extra_vars=vars)

            h.redirect_to(controller='ckanext.dataportaltheme.plugin:PortalController', action='dataportalAdmin')

        schema = logic.schema.update_configuration_schema()
        data = {}
        for key in schema:
            data[key] = config.get(key)

        vars = {'data': data, 'errors': {}}
        return base.render('admin/dataportal.html',
                           extra_vars=vars)

