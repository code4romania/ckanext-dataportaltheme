import json
from datetime import datetime

import requests
from cachetools.func import ttl_cache
from ckan import logic, plugins as p
from ckan.common import config, request as ckan_request, ugettext as _
from ckan.lib import base, helpers as h
from ckan.lib.navl import dictization_functions as dict_fns
from ckan.lib.plugins import DefaultDatasetForm, DefaultTranslation
from ckan.logic import schema
from ckan.views.home import CACHE_PARAMETERS
from flask import Blueprint

c = base.c
request = base.request


@ttl_cache(ttl=60 * 60)
def gettasks(params=None):
    params = params or {"state": "open"}
    url = config.get(
        "ckan.githubfeed.requesturl", "https://api.github.com/repos/code4romania/ckanext-dataportaltheme/issues"
    )
    r = requests.get(url=url, params=params)
    obj = json.loads(r.text)
    return obj


def all_groups():
    """Return a sorted list of the groups with the most datasets."""

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = logic.get_action("group_list")(data_dict={"all_fields": True})
    return groups


def similar_with(current_package):
    if len(current_package["groups"]) == 0:
        return []

    group = current_package["groups"][0]["name"]

    f_group_packages = logic.get_action("group_package_show")
    packages = f_group_packages(data_dict={"id": group, "limit": 3})

    # Delete current package from list if present
    idx_to_remove = -1
    for idx, package in enumerate(packages):
        if package["name"] == current_package["name"]:
            idx_to_remove = idx
            break
    if idx_to_remove != -1:
        packages.pop(idx_to_remove)

    return packages


def get_view_data(group):
    view_data = []
    site_url = config.get("ckan.site_url")

    if group:
        f_group_packages = logic.get_action("group_package_show")
        packages = f_group_packages(data_dict={"id": group, "limit": 8})
    else:
        packages = logic.get_action("current_package_list_with_resources")(data_dict={})

    ignored_views = ["text_view", "recline_graph_view", "recline_view"]
    for package in packages:
        for resource in package["resources"]:
            if len(view_data) > 7:
                break
            # Get view for resource
            views = logic.get_action("resource_view_list")(data_dict={"id": resource["id"]})
            # print(views)
            for view in views:
                if view["view_type"] in ignored_views:
                    continue
                url = "%s/dataset/%s/resource/%s/view/%s" % (site_url, package["name"], resource["id"], view["id"])
                link = "%s/dataset/%s/resource/%s" % (site_url, package["name"], resource["id"])
                view_data.append({"url": url, "name": view["title"], "link": link})
    return view_data


def generate_url(package):
    site_url = config.get("ckan.site_url")
    controller_type = "dataset" if h.ckan_version().split(".")[1] | int >= 9 else "package"
    relative_path = h.url_for_static(controller=controller_type, action="read", id=package["name"])
    return "".join([site_url, relative_path])


# BLUEPRINTS RULES START HERE:
def _get_config_form_items():
    # Styles for use in the form.select() macro.
    styles = [
        {"text": "Default", "value": "/base/css/main.css"},
        {"text": "Red", "value": "/base/css/red.css"},
        {"text": "Green", "value": "/base/css/green.css"},
        {"text": "Maroon", "value": "/base/css/maroon.css"},
        {"text": "Fuchsia", "value": "/base/css/fuchsia.css"},
    ]

    homepages = [
        {"value": "1", "text": "Introductory area, search, featured group and featured organization"},
        {"value": "2", "text": "Search, stats, introductory area, featured organization and featured group"},
        {"value": "3", "text": "Search, introductory area and stats"},
    ]

    items = [
        {"name": "ckan.site_title", "control": "input", "label": _("Site Title"), "placeholder": ""},
        {"name": "ckan.main_css", "control": "select", "options": styles, "label": _("Style"), "placeholder": ""},
        {"name": "ckan.site_description", "control": "input", "label": _("Site Tag Line"), "placeholder": ""},
        {
            "name": "ckan.site_logo",
            "control": "image_upload",
            "label": _("Site Tag Logo"),
            "placeholder": "",
            "upload_enabled": h.uploads_enabled(),
            "field_url": "ckan.site_logo",
            "field_upload": "logo_upload",
            "field_clear": "clear_logo_upload",
        },
        {"name": "ckan.site_about", "control": "markdown", "label": _("About"), "placeholder": _("About page text")},
        {
            "name": "ckan.site_intro_text",
            "control": "markdown",
            "label": _("Intro Text"),
            "placeholder": _("Text on home page"),
        },
        {
            "name": "ckan.site_custom_css",
            "control": "textarea",
            "label": _("Custom CSS"),
            "placeholder": _("Customisable css inserted into the page header"),
        },
        {
            "name": "ckan.homepage_style",
            "control": "select",
            "options": homepages,
            "label": _("Homepage"),
            "placeholder": "",
        },
    ]
    return items


def data_stats_esentiale():
    return base.render("dataStats/esentiale.html")


def data_stats_struct():
    return base.render("dataStats/struct.html")


def terms_and_conditions():
    return base.render("home/termsandconditions.html")


def contact_form():
    request_params = ckan_request.params
    url = "https://docs.google.com/forms/d/e/1FAIpQLSeGNW5FjBwauZLsf0Ar8P6SgbTdd0n5hRfCAJ-XKtzWQMSqRA/formResponse"
    form_data = {
        "entry.268426185": request_params["email"],
        "entry.782078158": request_params["message"],
        "draftResponse": [],
        "fvv": 1,
        "pageHistory": 0,
    }
    user_agent = {
        "Referer": "https://docs.google.com/forms/d/e/1FAIpQLSeGNW5FjBwauZLsf0Ar8P6SgbTdd0n5hRfCAJ-XKtzWQMSqRA/viewform",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36",
    }
    requests.post(url, data=form_data, headers=user_agent)
    return base.render("home/contactform.html")


def cookie_policy():
    return base.render("home/cookiepolicy.html")


def code_of_conduct():
    return base.render("home/codeofconduct.html")


def dataportal_admin():
    # items = self._get_config_form_items()
    data = request.POST
    if "save" in data:
        try:
            # really?
            data_dict = logic.clean_dict(
                dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.POST, ignore_keys=CACHE_PARAMETERS)))
            )
            del data_dict["save"]

            data = logic.get_action("config_option_update")({"user": c.user}, data_dict)
        except logic.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            vars = {"data": data, "errors": errors, "error_summary": error_summary}
            return base.render("admin/dataportal.html", extra_vars=vars)

        h.redirect_to(controller="ckanext.dataportaltheme.plugin:PortalController", action="dataportalAdmin")

    admin_schema = schema.update_configuration_schema()
    data = {}
    for key in admin_schema:
        data[key] = config.get(key)

    vars = {"data": data, "errors": {}}
    return base.render("admin/dataportal.html", extra_vars=vars)


def group_dashboard():
    group = request.GET.get("g", "")
    vars = {"selected_group": group}
    return base.render("home/index.html", extra_vars=vars)


class DataportalthemePlugin(p.SingletonPlugin, DefaultDatasetForm, DefaultTranslation):

    p.implements(p.IBlueprint, inherit=True)

    def get_blueprint(self):
        blueprint = Blueprint("dataportaltheme", self.__module__)
        rules = [
            ("/standard-date/esentiale", "data_stats_esentiale", data_stats_esentiale),
            ("/standard-date/structura", "data_stats_struct", data_stats_struct),
            ("/termsandconditions", "terms_and_conditions", terms_and_conditions),
            ("/contact-form", "contact_form", contact_form),
            ("/cookiepolicy", "cookie_policy", cookie_policy),
            ("/codeofconduct", "code_of_conduct", code_of_conduct),
            ("/ckan-admin/dataportal", "dataportal_admin", dataportal_admin),
            ("/group-dashboard", "group_dashboard", group_dashboard),
        ]

        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    def update_config_schema(self, config_schema):

        ignore_missing = logic.get_validator("ignore_missing")

        config_schema.update(
            {
                # This is an existing CKAN core configuration option, we are just
                # making it available to be editable at runtime
                "partner1_link": [ignore_missing],
                "partner1_logo": [ignore_missing],
                "partner2_link": [ignore_missing],
                "partner2_logo": [ignore_missing],
                "partner3_link": [ignore_missing],
                "partner3_logo": [ignore_missing],
                "partner4_link": [ignore_missing],
                "partner4_logo": [ignore_missing],
                "partner5_link": [ignore_missing],
                "partner5_logo": [ignore_missing],
                "partner6_link": [ignore_missing],
                "partner6_logo": [ignore_missing],
                "partner7_link": [ignore_missing],
                "partner7_logo": [ignore_missing],
                "partner8_link": [ignore_missing],
                "partner8_logo": [ignore_missing],
                "facebook_url": [ignore_missing],
                "twitter_url": [ignore_missing],
                "instagram_url": [ignore_missing],
                "linkedIn_url": [ignore_missing],
            }
        )

        return config_schema

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        p.toolkit.add_template_directory(config, "../templates")
        p.toolkit.add_public_directory(config, "../public")
        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        p.toolkit.add_resource("fanstatic", "../dataportaltheme")
        p.toolkit.add_resource("fanstatic", "../githubfeed")

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        p.toolkit.add_public_directory(config, "../public")

    def before_show(self, resource_dict):
        resource_dict["test"] = "test"
        return resource_dict

    def get_helpers(self):
        """Register the most_popular_groups() function above as a template
        helper function.

        """
        # Catch github API limit exception
        try:
            latest_issues = gettasks()[:3]
        except:
            latest_issues = []
        return {
            "all_groups": all_groups,
            "current_year": datetime.now().year,
            "githubfeed_latest": latest_issues,
            "githubfeed_getallissuesurl": config.get(
                "ckan.githubfeed.allissuesurl", "https://github.com/orgs/code4romania/projects/12"
            ),
            "similar": similar_with,
            "generate_url": generate_url,
            "get_view_data": get_view_data,
        }
