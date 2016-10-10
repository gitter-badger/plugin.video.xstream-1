import json

from resources.lib.site_plugin import SitePlugin

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib import logger

from resources.lib.bs_finalizer import *


class BurningSeriesPlugin(SitePlugin):
    site_identifier = 'burning_series_org'
    site_name = 'BurningSeries'

    url_main = 'https://www.bs.to/api/'
    url_cover = 'https://s.bs.to/img/cover/%s.jpg|encoding=gzip'

    def load(self):
        logger.info("Load %s" % self.site_name)
        self.gui.addFolder(self._create_gui_element('Alle Serien', 'show_series'))
        self.gui.addFolder(self._create_gui_element('A-Z', 'showCharacters'))
        self.gui.addFolder(self._create_gui_element('Zufall', 'showRandom'))
        self.gui.addFolder(self._create_gui_element('Suche', 'showSearch'))
        self.gui.setEndOfDirectory()

    def show_series(self):
        filter_char = self.params.getValue('char')
        if filter_char: filter_char = filter_char.lower()
        series = self._getJsonContent("series")
        total = len(series)
        for serie in series:
            title = serie["series"].encode('utf-8')
            if filter_char:
                if filter_char == '#':
                    if title[0].isalpha(): continue
                elif title[0].lower() != filter_char:
                    continue
            if self.params.getValue('specific') == 'Season':
                gui_element = self._create_gui_element(title, 'random_season')
            else:
                gui_element = self._create_gui_element(title, 'show_seasons')
            gui_element.setMediaType('tvshow')
            gui_element.setThumbnail(self.url_cover % serie["id"])
            # Load series description by iteration through the REST-Api (slow)
            # sDesc = _getJsonContent("series/%d/1" % int(serie['id']))
            # guiElement.setDescription(sDesc['series']['description'].encode('utf-8'))
            # sStart = str(sDesc['series']['start'])
            # if sStart != 'None':
            #   guiElement.setYear(int(sDesc['series']['start']))
            self.params.addParams({'seriesID': str(serie["id"]), 'Title': title})
            self.gui.addFolder(gui_element, self.params, iTotal=total)

        self.gui.setView('tvshows')
        self.gui.setEndOfDirectory()

    def _getJsonContent(self, url_part):
        request = cRequestHandler(self.url_main + url_part)
        mod_request(request, url_part)
        content = request.request()
        if content:
            return json.loads(content)
        else:
            return []