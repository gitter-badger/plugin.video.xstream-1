from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.config import cConfig


class SitePlugin(object):
    site_identifier = ''
    site_name = ''
    site_icon = None

    has_login = False

    def __init__(self):
        super(SitePlugin, self).__init__()
        self.params = ParameterHandler()
        self.gui = cGui()

    def load(self):
        raise NotImplementedError

    def _search(self, search_term, gui=None):
        return None

    def get_func(self, func_name):
        if hasattr(self, func_name):
            return getattr(self, func_name)
        return None

    @classmethod
    def _is_enabled(cls):
        return cConfig().getSetting('plugin_%s' % cls().site_identifier) == 'true'

    def _create_gui_element(self, title = '', func_name = None, site = None):
        if not site:
            site = self.site_identifier

        return cGuiElement(title, site, func_name)

    def _add_gui_element(self, title = '', func_name = None, site = None, params = None, gui = None):
        gui_element = self._create_gui_element(title, func_name, site)

        if not gui:
            gui = self.gui

        if params:
            for key in params:
                self.params.setParam(key, params[key])

        gui.addFolder(gui_element, self.params)