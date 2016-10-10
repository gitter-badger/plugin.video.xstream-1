# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.config import cConfig
from resources.lib import logger
import string
import json
import random
from resources.lib.bs_finalizer import *

# "Global" variables
SITE_IDENTIFIER = 'burning_series_org'
SITE_NAME = 'BurningSeries'
SITE_ICON = 'burning_series.png'

URL_MAIN = 'https://www.bs.to/api/'
URL_COVER = 'https://s.bs.to/img/cover/%s.jpg|encoding=gzip'

# Mainmenu
def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    oGui.addFolder(cGuiElement('Alle Serien', SITE_IDENTIFIER, 'showSeries'))
    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'showCharacters'))
    oGui.addFolder(cGuiElement('Zufall', SITE_IDENTIFIER, 'showRandom'))
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

### Mainmenu entries

# Show all series in a big list
def showSeries():
    oGui = cGui()
    oParams = ParameterHandler()
    sChar = oParams.getValue('char')
    if sChar: sChar = sChar.lower()
    series = _getJsonContent("series")
    total = len(series)
    for serie in series:
        sTitle = serie["series"].encode('utf-8')
        if sChar:
            if sChar == '#':
                if sTitle[0].isalpha(): continue
            elif sTitle[0].lower() != sChar: continue
        if oParams.getValue('specific') == 'Season':
            guiElement = cGuiElement(sTitle, SITE_IDENTIFIER, 'randomSeason')
        else:
            guiElement = cGuiElement(sTitle, SITE_IDENTIFIER, 'showSeasons')
        guiElement.setMediaType('tvshow')
        guiElement.setThumbnail(URL_COVER % serie["id"])
        # Load series description by iteration through the REST-Api (slow)
        #sDesc = _getJsonContent("series/%d/1" % int(serie['id']))
        #guiElement.setDescription(sDesc['series']['description'].encode('utf-8'))
        #sStart = str(sDesc['series']['start'])
        #if sStart != 'None':
        #   guiElement.setYear(int(sDesc['series']['start']))
        oParams.addParams({'seriesID' : str(serie["id"]), 'Title' : sTitle})
        oGui.addFolder(guiElement, oParams, iTotal = total)

    oGui.setView('tvshows')
    oGui.setEndOfDirectory()

# Show an alphabetic list 'A-Z' prepended by '#' for alphanumeric series
def showCharacters():
    oGui = cGui()
    oGuiElement = cGuiElement()
    oParams = ParameterHandler()
    oGuiElement = cGuiElement('#', SITE_IDENTIFIER, 'showSeries')
    oParams.setParam('char', '#')
    oGui.addFolder(oGuiElement, oParams)
    for letter in string.uppercase[:26]:
        oGuiElement = cGuiElement(letter, SITE_IDENTIFIER, 'showSeries')
        oParams.setParam('char', letter)
        oGui.addFolder(oGuiElement, oParams)
    oGui.setEndOfDirectory()

# Show the search dialog, return/abort on empty input
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(oGui, sSearchText)
    oGui.setEndOfDirectory()

### Helper functions

# Load a JSON object
def _getJsonContent(urlPart):
    request = cRequestHandler(URL_MAIN + urlPart)
    mod_request(request, urlPart)
    content = request.request()
    if content:
        return json.loads(content)
    else:
        return []

# Search for series using the requested string sSearchText
def _search(oGui, sSearchText):
    params = ParameterHandler()
    series = _getJsonContent("series")
    total = len(series)
    sSearchText = sSearchText.lower()
    for serie in series:
        sTitle = serie["series"].encode('utf-8')
        if sTitle.lower().find(sSearchText) == -1: continue
        guiElement = cGuiElement(sTitle, SITE_IDENTIFIER, 'showSeasons')
        guiElement.setMediaType('tvshow')
        guiElement.setThumbnail(URL_COVER % serie["id"])
        params.addParams({'seriesID' : str(serie["id"]), 'Title' : sTitle})
        oGui.addFolder(guiElement, params, iTotal = total)

# Show a list of seasons for a requested series, and movies if available
def showSeasons():
    oGui = cGui()
    params = ParameterHandler()
    sTitle = params.getValue('Title')
    seriesId = params.getValue('seriesID')
    sImdb = params.getValue('imdbID')

    logger.info("%s: show seasons of '%s' " % (SITE_NAME, sTitle))

    data = _getJsonContent("series/%s/1" % seriesId)
    rangeStart = not int(data["series"]["movies"])
    total = int(data["series"]["seasons"])
    for i in range(rangeStart, total + 1):
        seasonNum = str(i)
        if i is 0:
            seasonTitle = 'Film(e)'
            dialogType = 'showCinemaMovies'
        else:
            seasonTitle = '%s - Staffel %s' %(sTitle, seasonNum)
            if params.getValue('specific') == 'Episode':
                dialogType = 'randomEpisode'
            else:
                dialogType = 'showEpisodes'
        guiElement = cGuiElement(seasonTitle, SITE_IDENTIFIER, dialogType)
        guiElement.setMediaType('season')
        guiElement.setSeason(seasonNum)
        guiElement.setTVShowTitle(sTitle)

        params.setParam('Season', seasonNum)
        guiElement.setThumbnail(URL_COVER % data["series"]["id"])
        oGui.addFolder(guiElement, params, iTotal = total)
    oGui.setView('seasons')
    oGui.setEndOfDirectory()

# Show episodes of a requested season for a series
def showEpisodes():
    oGui = cGui()
    oParams = ParameterHandler()
    sShowTitle = oParams.getValue('Title')
    seriesId = oParams.getValue('seriesID')
    sImdb = oParams.getValue('imdbID')
    sSeason = oParams.getValue('Season')

    logger.info("%s: show episodes of '%s' season '%s' " % (SITE_NAME, sShowTitle, sSeason))

    data = _getJsonContent("series/%s/%s" % (seriesId, sSeason))
    total = len(data['epi'])
    for episode in data['epi']:
        title = "%d - " % int(episode['epi'])
        if episode['german']:
            title += episode['german'].encode('utf-8')
        else:
            title += episode['english'].encode('utf-8')
        guiElement = cGuiElement(title, SITE_IDENTIFIER, 'showHosters')
        guiElement.setMediaType('episode')
        guiElement.setSeason(data['season'])
        guiElement.setEpisode(episode['epi'])
        guiElement.setTVShowTitle(sShowTitle)
        guiElement.setThumbnail(URL_COVER % data["series"]["id"])
        oParams.setParam('EpisodeNr', episode['epi'])
        oGui.addFolder(guiElement, oParams, bIsFolder = False, iTotal = total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def showCinemaMovies():
    oGui = cGui()
    oParams = ParameterHandler()
    sShowTitle = oParams.getValue('Title')
    seriesId = oParams.getValue('seriesID')
    sImdb = oParams.getValue('imdbID')

    data = _getJsonContent("series/%s/0" % (seriesId))
    total = len(data['epi'])

    for movie in data['epi']:
        if movie['german']:
            title = movie['german'].encode('utf-8')
        else:
            title = movie['english'].encode('utf-8')
        guiElement = cGuiElement(title, SITE_IDENTIFIER, 'showHosters')
        guiElement.setMediaType('movie')
        guiElement.setTitle(title)
        guiElement.setThumbnail(URL_COVER % data["series"]["id"])
        oParams.setParam('EpisodeNr', movie['epi'])
        oGui.addFolder(guiElement, oParams, bIsFolder = False, iTotal = total)
    oGui.setView('movie')
    oGui.setEndOfDirectory()
    
def showRandom():
    oGui = cGui()
    oParams = ParameterHandler()

    oGui.addFolder(cGuiElement('Zufällige Serie', SITE_IDENTIFIER, 'randomSerie'))
    oParams.setParam('specific', 'Season')
    oGui.addFolder(cGuiElement('Zufällige Staffel', SITE_IDENTIFIER, 'randomSeason'), oParams)
    oParams.setParam('specific', 'Episode')
    oGui.addFolder(cGuiElement('Zufällige Episode', SITE_IDENTIFIER, 'randomEpisode'), oParams)

    oGui.setEndOfDirectory()

def randomSerie():
    oGui = cGui()
    oParams = ParameterHandler()
    serie = random.choice(_getJsonContent('series'))
    sTitle = serie["series"].encode('utf-8')
    guiElement = cGuiElement(sTitle, SITE_IDENTIFIER, 'showSeasons')
    guiElement.setMediaType('tvshow')
    guiElement.setThumbnail(URL_COVER % serie["id"])
    oParams.addParams({'seriesID': str(serie["id"]), 'Title': sTitle})
    oGui.addFolder(guiElement, oParams, iTotal=1)

    oGui.setEndOfDirectory()

def randomSeason():
    oGui = cGui()
    oParams = ParameterHandler()
    if oParams.getValue('specific') == 'Season' and not oParams.getValue('seriesID'):
        showSeries()
        return

    data = _getJsonContent("series/%s/1" % oParams.getValue('seriesID'))

    seasons = int(data["series"]["seasons"])+1

    randomSeason = random.randrange(1, seasons, 1)

    seasonNum = str(randomSeason)
    seasonTitle = '%s - Staffel %s' % (oParams.getValue('Title'), seasonNum)
    dialogType = 'showEpisodes'
    guiElement = cGuiElement(seasonTitle, SITE_IDENTIFIER, dialogType)
    guiElement.setMediaType('season')
    guiElement.setSeason(seasonNum)
    guiElement.setTVShowTitle(oParams.getValue('Title'))

    oParams.setParam('Season', seasonNum)
    guiElement.setThumbnail(URL_COVER % data["series"]["id"])
    oGui.addFolder(guiElement, oParams, iTotal=1)

    oGui.setEndOfDirectory()

def randomEpisode():
    oGui = cGui()
    oParams = ParameterHandler()
    if oParams.getValue('specific') == 'Episode' and not oParams.getValue('seriesID'):
        showSeries()
        return
    elif oParams.getValue('seriesID') and not oParams.getValue('Season'):
        showSeasons()
        return
    else:
        series = {'id': oParams.getValue('seriesID'), 'series': oParams.getValue('Title')}

    season = _getJsonContent("series/%s/1" % series['id'])
    randomEpisodeNr = (random.choice(season['epi']))['epi']
    randomEpisode = filter(lambda person: person['epi'] == randomEpisodeNr, season['epi'])[0]

    Title = season['series']['series'].encode('utf-8') + ' - Staffel ' + str(season['season']) + ' - '
    if randomEpisode['german']:
        Title += randomEpisode['german'].encode('utf-8')
    else:
        Title += randomEpisode['english'].encode('utf-8')

    guiElement = cGuiElement(Title, SITE_IDENTIFIER, 'showHosters')
    guiElement.setMediaType('episode')
    guiElement.setEpisode(randomEpisodeNr)
    guiElement.setSeason(season['season'])
    guiElement.setTVShowTitle(series['series'])
    guiElement.setThumbnail(URL_COVER % int(season['series']['id']))
    oParams.setParam('EpisodeNr', randomEpisodeNr)
    oParams.setParam('seriesID', season['series']['id'])
    oParams.setParam('Season', season['season'])
    oGui.addFolder(guiElement, oParams, bIsFolder=False, iTotal=1)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()
    return
 
# Show a hoster dialog for a requested episode
def showHosters():
    oParams= ParameterHandler()
    sTitle = oParams.getValue('Title')
    seriesId = oParams.getValue('seriesID')
    season = oParams.getValue('Season')
    episode = oParams.getValue('EpisodeNr')

    data = _getJsonContent("series/%s/%s/%s" % (seriesId, season, episode))
    hosters = []
    for link in data['links']:
        hoster = dict()
        hoster['link'] = URL_MAIN + 'watch/' + link['id']
        hoster['name'] = link['hoster']
        if hoster['name'] == "OpenLoadHD":
            hoster['name'] = "OpenLoad";
        hoster['displayedName'] = link['hoster']
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

# Load a url for a requested host
def getHosterUrl(sUrl = False):
    oParams = ParameterHandler()
    #sTitle = oParams.getValue('Title')
    #sHoster = oParams.getValue('Hoster')
    if not sUrl: sUrl = oParams.getValue('url')
    data = _getJsonContent(sUrl.replace(URL_MAIN, ''))
    results = []
    result = {}
    if data['fullurl'].startswith('http'):
        result['streamUrl'] = data['fullurl']
    else:
        result['streamID'] = data['url']
        result['host'] = data['hoster']
        if result['host'] == "OpenLoadHD":
            result['host'] = "OpenLoad";
    result['resolved'] = False
    results.append(result)
    return results