from datetime import datetime

from ckan import logic, plugins
from ckan.common import config
from ckan.lib.plugins import DefaultDatasetForm, DefaultTranslation
from ckan.plugins import toolkit

from .views import all_groups, dpt_blueprint, generate_url, get_github_issues, get_view_data, similar_with


class DataportalthemePlugin(plugins.SingletonPlugin, DefaultDatasetForm, DefaultTranslation):

    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def get_blueprint(self):
        return [dpt_blueprint]

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
        toolkit.add_template_directory(config, "../templates")

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, "../public")

        # Register this plugin's assets directory with CKAN.
        # Here, 'assets' is the path to the webassets directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this assets directory from CKAN
        # templates.
        toolkit.add_resource("../assets", "dataportaltheme")

    def before_show(self, resource_dict):
        resource_dict["test"] = "test"
        return resource_dict

    def get_helpers(self):
        """Register the most_popular_groups() function above as a template
        helper function.

        """
        # Catch github API limit exception
        try:
            latest_issues = get_github_issues()[:3]
        except Exception:
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
