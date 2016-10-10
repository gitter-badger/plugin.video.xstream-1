# -*- coding: utf-8 -*-
import string
import json
import random

from resources.lib.site_plugin import SitePlugin

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib import logger
from resources.lib.local_storage import LocalStorage

from resources.lib.bs_finalizer import *


class BurningSeriesPlugin(SitePlugin, LocalStorage):
    site_identifier = 'burning_series_org'
    site_name = 'BurningSeries'

    url_main = 'https://www.bs.to/api/'
    url_cover = 'https://s.bs.to/img/cover/%s.jpg|encoding=gzip'

    def load(self):
        self.clear()

        self._add_gui_element('Alle Serien', 'show_series')
        self._add_gui_element('A-Z', 'show_characters')
        self._add_gui_element('Zufall', 'show_random')
        self._add_gui_element('Suche', 'show_search')
        self.gui.setEndOfDirectory()

    def _search(self, search_term, gui=None):
        if not gui:
            gui = self.gui

        series = self._getJsonContent("series")
        total = len(series)
        search_term = search_term.lower()
        for serie in series:
            title = serie["series"].encode('utf-8')
            if title.lower().find(search_term) == -1: continue
            gui_element = self._create_gui_element(title, 'show_seasons')
            gui_element.setMediaType('tvshow')
            gui_element.setThumbnail(self.url_cover % serie["id"])
            self.params.addParams({'series_id': str(serie["id"]), 'title': title})
            gui.addFolder(gui_element, self.params, iTotal=total)

    # region Helper

    def _getJsonContent(self, url_part):
        request = cRequestHandler(self.url_main + url_part)
        mod_request(request, url_part)
        content = request.request()
        if content:
            return json.loads(content)
        else:
            return []

    # endregion

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
            self.params.addParams({'series_id': str(serie["id"]), 'title': title})
            self.gui.addFolder(gui_element, self.params, iTotal=total)

        self.gui.setView('tvshows')
        self.gui.setEndOfDirectory()

    def show_characters(self):
        self._add_gui_element('#', 'show_series', params={'char': '#'})
        for letter in string.uppercase[:26]:
            self._add_gui_element(letter, 'show_series', params={'char': letter})
        self.gui.setEndOfDirectory()

    def show_random(self):
        self._add_gui_element('Zufällige Serie', 'random_serie')
        self._add_gui_element('Zufällige Staffel', 'random_season', params={'specific': 'Season'})
        self._add_gui_element('Zufällige Episode', 'random_episode', params={'specific': 'Episode'})
        self.gui.setEndOfDirectory()

    def show_search(self):
        search_term = self.gui.showKeyBoard()
        if not search_term: return
        self._search(search_term)
        self.gui.setEndOfDirectory()

    def show_seasons(self):
        title = self.params.getValue('title')
        series_id = self.params.getValue('series_id')

        logger.info("%s: show seasons of '%s' " % (self.site_name, title))

        data = self._getJsonContent("series/%s/1" % series_id)
        range_start = not int(data["series"]["movies"])
        total = int(data["series"]["seasons"])
        for i in range(range_start, total + 1):
            season_num = str(i)
            if i is 0:
                season_title = 'Film(e)'
                func_name = 'show_cinema_movies'
            else:
                season_title = '%s - Staffel %s' % (title, season_num)
                if self.params.getValue('specific') == 'Episode':
                    func_name = 'random_episode'
                else:
                    func_name = 'show_episodes'
            gui_element = self._create_gui_element(season_title, func_name)
            gui_element.setMediaType('season')
            gui_element.setSeason(season_num)
            gui_element.setTVShowTitle(title)

            self.params.setParam('season_num', season_num)
            gui_element.setThumbnail(self.url_cover % data["series"]["id"])
            self.gui.addFolder(gui_element, self.params, iTotal=total)
        self.gui.setView('seasons')
        self.gui.setEndOfDirectory()

    def show_episodes(self):
        title = self.params.getValue('title')
        series_id = self.params.getValue('series_id')
        season_num = self.params.getValue('season_num')

        logger.info("%s: show episodes of '%s' season '%s' " % (self.site_name, title, season_num))

        data = self._getJsonContent("series/%s/%s" % (series_id, season_num))
        total = len(data['epi'])
        for episode in data['epi']:
            title = "%d - " % int(episode['epi'])
            if episode['german']:
                title += episode['german'].encode('utf-8')
            else:
                title += episode['english'].encode('utf-8')
            gui_element = self._create_gui_element(title, 'show_hosters')
            gui_element.setMediaType('episode')
            gui_element.setSeason(data['season'])
            gui_element.setEpisode(episode['epi'])
            gui_element.setTVShowTitle(title)
            gui_element.setThumbnail(self.url_cover % data["series"]["id"])
            self.params.setParam('episode_num', episode['epi'])
            self.gui.addFolder(gui_element, self.params, bIsFolder=False, iTotal=total)
        self.gui.setView('episodes')
        self.gui.setEndOfDirectory()

    def random_serie(self):
        serie = random.choice(self._getJsonContent('series'))
        title = serie["series"].encode('utf-8')
        guiElement = self._create_gui_element(title, 'showSeasons')
        guiElement.setMediaType('tvshow')
        guiElement.setThumbnail(self.url_cover % serie["id"])
        self.params.addParams({'series_id': str(serie["id"]), 'title': title})
        self.gui.addFolder(guiElement, self.params, iTotal=1)

        self.gui.setEndOfDirectory()

    def random_season(self):
        if self.params.getValue('specific') == 'Season' and not self.params.getValue('series_id'):
            self.show_series()
            return

        data = self._getJsonContent("series/%s/1" % self.params.getValue('series_id'))

        seasons = int(data["series"]["seasons"]) + 1

        random_season = random.randrange(1, seasons, 1)

        season_num = str(random_season)
        title = '%s - Staffel %s' % (self.params.getValue('title'), season_num)
        gui_element = self._create_gui_element(title, 'showEpisodes')
        gui_element.setMediaType('season')
        gui_element.setSeason(season_num)
        gui_element.setTVShowTitle(self.params.getValue('title'))

        self.params.setParam('season_num', season_num)
        gui_element.setThumbnail(self.url_cover % data["series"]["id"])
        self.gui.addFolder(gui_element, self.params, iTotal=1)

        self.gui.setEndOfDirectory()

    def random_episode(self):
        if self.params.getValue('specific') == 'episode_num' and not self.params.getValue('series_id'):
            self.show_series()
            return
        elif self.params.getValue('series_id') and not self.params.getValue('season_num'):
            self.show_seasons()
            return
        else:
            series = {'id': self.params.getValue('series_id'), 'series': self.params.getValue('title')}

        season = self._getJsonContent("series/%s/1" % series['id'])
        print 'BSDEB: '
        print season
        random_episode_num = (random.choice(season['epi']))['epi']
        random_episode = filter(lambda person: person['epi'] == random_episode_num, season['epi'])[0]

        title = season['series']['series'].encode('utf-8') + ' - Staffel ' + str(season['season']) + ' - '
        if random_episode['german']:
            title += random_episode['german'].encode('utf-8')
        else:
            title += random_episode['english'].encode('utf-8')

        gui_element = self._create_gui_element(title, 'show_hosters')
        gui_element.setMediaType('episode')
        gui_element.setEpisode(randomEpisodeNr)
        gui_element.setSeason(season['season'])
        gui_element.setTVShowTitle(series['series'])
        gui_element.setThumbnail(self.url_cover % int(season['series']['id']))
        self.params.setParam('episode_num', random_episode_num)
        self.params.setParam('series_id', season['series']['id'])
        self.params.setParam('season_num', season['season'])
        self.gui.addFolder(gui_element, self.params, bIsFolder=False, iTotal=1)

        self.gui.setView('episodes')
        self.gui.setEndOfDirectory()
        return

    # Show a hoster dialog for a requested episode
    def show_hosters(self):
        series_id = self.params.getValue('series_id')
        season_num = self.params.getValue('season_num')
        episode_num = self.params.getValue('episode_num')

        data = self._getJsonContent("series/%s/%s/%s" % (series_id, season_num, episode_num))
        hosters = []
        for link in data['links']:
            hoster = dict()
            hoster['link'] = self.url_main + 'watch/' + link['id']
            hoster['name'] = link['hoster']
            if hoster['name'] == "OpenLoadHD":
                hoster['name'] = "OpenLoad"
            hoster['displayedName'] = link['hoster']
            hosters.append(hoster)
        if hosters:
            hosters.append('get_hoster_url')
        return hosters

    # Load a url for a requested host
    def get_hoster_url(self, sUrl=False):
        if not sUrl: sUrl = self.params.getValue('url')
        data = self._getJsonContent(sUrl.replace(self.url_main, ''))
        results = []
        result = {}
        if data['fullurl'].startswith('http'):
            result['streamUrl'] = data['fullurl']
        else:
            result['streamID'] = data['url']
            result['host'] = data['hoster']
            if result['host'] == "OpenLoadHD":
                result['host'] = "OpenLoad"
        result['resolved'] = False
        results.append(result)
        return results