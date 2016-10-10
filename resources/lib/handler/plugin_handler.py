from new_sites import *

from resources.lib.site_plugin import SitePlugin
from resources.lib import common, logger


class PluginHandler(object):
    def __init__(self):
        pass

    def get_plugins(self):
        plugins = []

        classes = SitePlugin.__class__.__subclasses__(SitePlugin)
        for site in classes:
            if site._is_enabled():
                plugins.append(site())

        return plugins

    def get_plugin(self, plugin_name):
        plugins = self.get_plugins()

        for plugin in plugins:
            if plugin.site_identifier == plugin_name:
                return plugin
        return None