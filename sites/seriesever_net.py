# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from xbmc import translatePath

import os
import re
import json
import urllib
import base64
import xbmcaddon

SITE_IDENTIFIER = 'seriesever_net'
SITE_NAME = 'SeriesEver'
SITE_ICON = 'seriesever.png'

URL_MAIN = 'http://seriesever.net/'
URL_SERIES = URL_MAIN + 'andere-serien/'
URL_ANIMES = URL_MAIN + 'anime/'
URL_MOVIES = URL_MAIN + 'filme/'

URL_GENRE = URL_MAIN + 'genre/'

URL_SEARCH = URL_MAIN + 'service/search'
URL_GETVIDEOPART = URL_MAIN + 'service/get_video_part'
URL_PLAYER = URL_MAIN + 'play/plugins/playerphp.php'


def load():
    oParams = ParameterHandler()

    oGui = cGui()
    oParams.setParam('mediaType', 'series')
    oGui.addFolder(cGuiElement('Neue Episoden', SITE_IDENTIFIER, 'showNewEpisodesMenu'), oParams)
    oGui.addFolder(cGuiElement('Alle Serien', SITE_IDENTIFIER, 'showSeriesMenu'), oParams)
    oGui.addFolder(cGuiElement('Animes', SITE_IDENTIFIER, 'showAnimesMenu'), oParams)
    oParams.setParam('mediaType', 'movies')
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMoviesMenu'), oParams)
    oParams.setParam('mediaType', 'series')
    oGui.addFolder(cGuiElement('Genres', SITE_IDENTIFIER, 'showGenresMenu'), oParams)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'), oParams)
    oGui.setEndOfDirectory()


def __getHtmlContent(sUrl=None):
    oParams = ParameterHandler()
    # Test if a url is available and set it
    if sUrl is None and not oParams.exist('sUrl'):
        logger.error("There is no url we can request.")
        return False
    else:
        if sUrl is None:
            sUrl = oParams.getValue('sUrl')
    # Make the request
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1')
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Accept', '*/*')

    return oRequest.request()


def showNewEpisodesMenu():
    logger.info('load showNewEpisodesMenu')
    showFrontPage()


def showSeriesMenu():
    logger.info('load showSeriesMenu')
    showSeries(URL_SERIES)


def showAnimesMenu():
    logger.info('load showAnimesMenu')
    showSeries(URL_ANIMES)


def showMoviesMenu():
    logger.info('load showMoviesMenu')
    showSeries(URL_MOVIES)


def showSearch():
    logger.info('load showSearch')
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False and sSearchText != ''):
        _search(oGui, sSearchText)
    else:
        return
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    params = ParameterHandler()
    oRequestHandler = cRequestHandler(URL_SEARCH + '?q=' + sSearchText)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    sHtmlContent = oRequestHandler.request()
    series = json.loads(sHtmlContent)

    if series:
        total = len(series)
        for serie in series:
            sTitle = serie["name"].encode('utf-8')
            guiElement = cGuiElement(sTitle, SITE_IDENTIFIER, 'showSeasons')
            guiElement.setMediaType('tvshow')
            params.addParams({'sUrl': serie['url'], 'Title': sTitle})
            oGui.addFolder(guiElement, params, iTotal=total)


def showGenresMenu():
    logger.info('load displayGenreSite')
    oParams = ParameterHandler()
    sPattern = '<li><a href="' + URL_GENRE + '(.*?).html".*?>(.*?)</a></li>'

    # request
    sHtmlContent = __getHtmlContent(URL_MAIN)
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            guiElement = cGuiElement(aEntry[1], SITE_IDENTIFIER, 'showSeries')
            #guiElement.setMediaType('fGenre') #not necessary
            oParams.addParams({'sUrl': URL_GENRE + aEntry[0] + '/', 'iPage': 1})
            oGui.addFolder(guiElement, oParams)

    oGui.setEndOfDirectory()


def showSeries(sUrl=False):
    logger.info('load showSeries')
    oParams = ParameterHandler()

    if not sUrl:
        sUrl = oParams.getValue('sUrl')

    sPagePattern = '<a href="' + sUrl + '(\d+).html">'

    # request
    sHtmlContent = __getHtmlContent(sUrl)
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPagePattern)

    pages = 1
    if aResult[0]:
        if representsInt(aResult[1][-1]):
            pages = aResult[1][-1]

    oGui = cGui()

    # because sometimes 2 pages have the same content
    dupeCheck = []
    for x in range(1, int(pages) + 1):
        dupeCheck = showSeriesPage(oGui, sUrl, x, dupeCheck)

    oGui.setView('tvshows')
    oGui.setEndOfDirectory()


def showFrontPage():
    oParams = ParameterHandler()
    sPattern = '<div class="box-container">.*?<a href="(.*?)".*?Staffel (.*?) Episode (.*?)".*?src="(http://seriesever.net/uploads/posters/thumb/.*?)".*?alt="(.*?)"'

    # request
    sHtmlContent = __getHtmlContent(URL_MAIN)
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    if (aResult[0] == True):
        for link, season, episode, img, title in aResult[1]:
            guiElement = cGuiElement('%s: Season %s - Episode %s' % (title, season, episode), SITE_IDENTIFIER, 'showHosters')
            guiElement.setMediaType('episode')
            guiElement.setSeason(season)

            # Special fix for non-int episode numbers (like Attack on Titan 13.5)
            # Can't even check this on thetvdb.com, because AOT 13.5 for example is Season 0 Episode 1
            # May I can use "<airsbefore_episode>" and "<airsbefore_season>" for metadata
            if representsInt(episode):
                guiElement.setEpisode(episode)

            guiElement.setTVShowTitle(title)
            guiElement.setThumbnail(img)

            oParams.setParam('sUrl', link)
            oGui.addFolder(guiElement, oParams, bIsFolder=False)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def showSeriesPage(oGui, sUrl, iPage, dupeCheck):
    oParams = ParameterHandler()
    sPattern = '<div class="box-container">.*?<a href="(.*?)".*?src="(.*?)".*?alt="(.*?)"'

    # request
    if int(iPage) == 1:
        sHtmlContent = __getHtmlContent(sUrl)
    else:
        sHtmlContent = __getHtmlContent(sUrl + str(iPage))
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for link, img, title in aResult[1]:
            if title in dupeCheck: continue
            if 'movies' in oParams.getValue('mediaType'):
                guiElement = cGuiElement(title, SITE_IDENTIFIER, 'showMovie')
            else:
                guiElement = cGuiElement(title, SITE_IDENTIFIER, 'showSeasons')
            guiElement.setMediaType('tvshow')
            guiElement.setThumbnail(img)
            oParams.addParams({'sUrl': link, 'Title': title})
            oGui.addFolder(guiElement, oParams)
            dupeCheck.append(title)
    return dupeCheck


def showSeasons():
    logger.info('load showSeasons')
    oParams = ParameterHandler()
    sTitle = oParams.getValue('Title')
    sPattern = '<a href="#season-(.*?)" data-parent=".*?>(.*?)</a>'

    # request
    sHtmlContent = __getHtmlContent()
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    if aResult[0]:
        for sId, seasonNum in aResult[1]:
            guiElement = cGuiElement('%s - Staffel %s' % (sTitle, seasonNum), SITE_IDENTIFIER, 'showEpisodes')
            guiElement.setMediaType('season')
            guiElement.setSeason(seasonNum)
            guiElement.setTVShowTitle(sTitle)

            oParams.setParam('Season', seasonNum)
            oGui.addFolder(guiElement, oParams)

    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showMovie():
    logger.info('load showMovie')
    oParams = ParameterHandler()
    sPattern = 'class="list-group-item".*?<img.*?src="(.*?)".*?itemprop="image".*?<span itemprop="name">(.*?)</span>.*?class="episode-name".*?href="(.*?)".*?title="(.*?)"'

    # request
    sHtmlContent = __getHtmlContent()
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    if (aResult[0] == True):
        for img, eNr, link, title in aResult[1]:
            guiElement = cGuiElement('Film %s - %s' % (eNr, title), SITE_IDENTIFIER, 'showHosters')
            guiElement.setThumbnail(img)
            guiElement.setMediaType('movie')
            guiElement.setTVShowTitle(title)
            oParams.addParams({'sUrl': link, 'from_moviesever': True})
            oGui.addFolder(guiElement, oParams, bIsFolder=False)

    oGui.setView('movies')
    oGui.setEndOfDirectory()

def showEpisodes():
    logger.info('load showEpisodes')
    oParams = ParameterHandler()
    sTitle = oParams.getValue('Title')
    sSeason = oParams.getValue('Season')

    sPattern = 'class="list-group-item".*?<span itemprop="name">Staffel ' + sSeason + ' Episode(?:[\s]*)(.*?)</span>.*?<a class="episode-name" href="(.*?)" title="(.*?)"'

    # request
    sHtmlContent = __getHtmlContent()
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    if (aResult[0] == True):
        for eNr, link, title in aResult[1]:
            guiElement = cGuiElement('Episode %s - %s' % (eNr, title), SITE_IDENTIFIER, 'showHosters')
            guiElement.setMediaType('episode')
            guiElement.setSeason(sSeason)

            # Special fix for non-int episode numbers (like Attack on Titan 13.5)
            # Can't even check this on thetvdb.com, because AOT 13.5 for example is Season 0 Episode 1
            # May I can use "<airsbefore_episode>" and "<airsbefore_season>" for metadata
            if representsInt(eNr):
                guiElement.setEpisode(eNr)

            guiElement.setTVShowTitle(sTitle)

            oParams.setParam('sUrl', link)
            oGui.addFolder(guiElement, oParams, bIsFolder=False)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def showHosters():
    logger.info('load showHosters')
    oParams = ParameterHandler()
    hosters = []
    try:
        sHtmlContent = __getHtmlContent()
        video_id = re.findall('var video_id.*?(\d+)', sHtmlContent)[0]
        # 720p seems to be the best on this site, even if 1080p is avaible for selection, only the 720p stream2k links contain a 1080p stream
        part_name = '720p'
        parts = re.findall('class="changePart" data-part="(.*?)">', sHtmlContent)
        if len(parts) == 1:
            part_name = parts[0]
        # last part is usually 1080p which is premium only
        #if oParams.exist('from_moviesever') and len(parts) == 2:
        #    part_name = parts[1]

        app = re.findall('<script src="(%sassets/js/app.js.*?)"></script>' % URL_MAIN, sHtmlContent)

        domain_list = []
        #try:
        #    domain_list = __get_domain_list(app, domain_list)
        #except:
        #    logger.info('Could not get domain list')
        #if not domain_list:
        #    domain_list = ['se1.seriesever.net', 'se2.seriesever.net']
        #import random
        #random.shuffle(domain_list)

        json_data = __getVideoPage(video_id, part_name, '0')

        try:
            part_count = json_data['part_count']
        except:
            part_count = 0

        hosters = parseHosterResponse(json_data, hosters)

        if part_count > 1:
            for i in range(1, part_count):
                json_data = __getVideoPage(video_id, part_name, str(i))
                hosters = parseHosterResponse(json_data, hosters)

        hosters.sort()

    except Exception, e:
        logger.error(e)
    if hosters:
        hosters.append('getHosterUrl')

    return hosters


def parseHosterResponse(json_data, hosters):
    if (json_data['part']['source'] != 'url') and (json_data['part']['source'] != 'other'):
        logger.error("Unknown data: %s" % json_data['part']['source'])
        return

    code = None
    try:
        code = json_data['part']['code']
    except:
        pass

    if code:
        hoster = dict()

        if json_data['part']['source'] == 'url':
            if "http" not in code:
                hoster['link'] = __decodeHash(code)
            else:
                hoster['link'] = code
        elif json_data['part']['source'] == 'other':
            link1 = re.findall('src="(http.*?)"', code)[0]

            if "/play/old/seframer.php" in link1:
                hoster['link'] = urllib.unquote(__getOldurl(link1))
            else:
                hoster['link'] = link1

        hname = 'Unknown Hoster'
        try:
            hname = re.compile('^(?:https?:\/\/)?(?:www\.)?(?:[^@\n]+@)?([^:\/\n]+)', flags=re.I | re.M).findall(hoster['link'])
        except Exception, e:
            logger.error(e)

        hoster['name'] = hname[0]
        hoster['link'] = hoster['link']

        hosters.append(hoster)

    return hosters


def __decodeHash(sHash):
    sHash = sHash.replace("!BeF", "R")
    sHash = sHash.replace("@jkp", "Ax")
    try:
        url = base64.b64decode(sHash)
        return url
    except:
        logger.error("Invalid Base64: %s" % sHash)


def getHosterUrl(sUrl=False):
    oParams = ParameterHandler()

    if not sUrl:
        sUrl = oParams.getValue('url')

    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results


def __getVideoPage(video_id, part_name, page):
    oRequestHandler = cRequestHandler(URL_GETVIDEOPART)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addParameters('video_id', video_id)
    oRequestHandler.addParameters('part_name', part_name)
    oRequestHandler.addParameters('page', page)
    sHtmlContentTmp = oRequestHandler.request()
    json_data = json.loads(sHtmlContentTmp)
    return json_data


def __get_domain_list(app, domain_list):
    sHtmlContent = __getHtmlContent(app)
    domains = re.findall("var domains\s*?=\s*?\[(.*?)\]", sHtmlContent)[0]
    domains = re.findall("'(.*?)'", domains)
    for domain in domains:
        domain_list.append(domain)
    return domain_list


def __getOldurl(sLink):
    sHtmlContent = __getHtmlContent(sLink)
    url = re.findall('url="(.*?)"', sHtmlContent)

    if len(url) == 0:
        url = re.findall('src="(.*?)"', sHtmlContent)
        if len(url) == 0:
            logger.error("Unknown Response: %s" % sHtmlContent)
        else:
            if "play/se.php" in url[0]:
                sHtmlContent = __getHtmlContent(url[0])
                sHash = re.findall('link:"(.*?)"', sHtmlContent)[0]
                return __decodeHash(sHash)
            else:
                logger.error("Unknown url: %s" % url)
    else:
        return url[0]