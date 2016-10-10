# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import ast

import re, json
from datetime import datetime

SITE_IDENTIFIER = 'cine_to'
SITE_NAME = 'Cine'
SITE_ICON = 'cine_to.png'

URL_PROTOCOL = 'https:'
URL_MAIN = URL_PROTOCOL + '//cine.to'
URL_SEARCH = URL_PROTOCOL + '//cine.to/request/search'
URL_LINKS = URL_PROTOCOL + '//cine.to/request/links'
URL_OUT = URL_PROTOCOL + '//cine.to/out/%s'

SEARCH_DICT = {'kind':'all', 'genre':'0', 'rating':'1', 'year[]': ['1913', '2016'], 'term':'', 'page':'1', 'count' : '25'}
QUALITY_ENUM = {'LD':0,'SD':3,'HD':4}

def load():
    logger.info("Load %s" % SITE_NAME)

    oGui = cGui()
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showMovieMenu():
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = '<input[^>]*name="kind"[^>]*value="(.*?)"[^>]*>' # kind
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)

    if not isMatch:
        return

    oGui = cGui()
    params = ParameterHandler()
    for sKind in aResult:
        params.setParam('kind', sKind)
        oGui.addFolder(cGuiElement(sKind.title(), SITE_IDENTIFIER, 'searchRequest'), params)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenresMenu'))
    oGui.addFolder(cGuiElement('Erscheinungszeitraum', SITE_IDENTIFIER, 'showYearSearch'))
    oGui.addFolder(cGuiElement('Geringstes Rating', SITE_IDENTIFIER, 'showRatingSearch'))
    oGui.setEndOfDirectory()

def showGenresMenu():
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = '<ul[^>]*id="genres"[^>]*>(.*?)</ul>' # genre-ul
    isMatch, sContainer = cParser().parseSingleResult(sHtmlContent, pattern)

    if not isMatch:
        return

    pattern = '<a[^>]*data-id="(\d+)"[^>]*href="[^"]*"[^>]*>([^<]*)<s' # id / title
    isMatch, aResult = cParser().parse(sContainer, pattern)

    if not isMatch:
        return

    oGui = cGui()
    params = ParameterHandler()
    for sGenreId, sTitle in aResult:
        params.setParam('genre', sGenreId)
        oGui.addFolder(cGuiElement(sTitle.strip(), SITE_IDENTIFIER, 'searchRequest'), params)
    oGui.setEndOfDirectory()

def searchRequest(dictFilter = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()

    dictFilter = {}
    for (prop, val) in SEARCH_DICT.items():
        parmVal = params.getValue(prop)
        parmVal = ast.literal_eval(parmVal) if prop == 'year[]' and parmVal else parmVal # yes a bit ugly
        dictFilter[prop] = parmVal if parmVal else val
        params.setParam(prop, dictFilter[prop])

    oResponse = _getJSonResponse(URL_SEARCH, dictFilter)

    if 'entries' not in oResponse or len(oResponse['entries']) == 0:
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    sLanguage = _getPrefLanguage()

    total = len (oResponse['entries'])
    for aEntry in oResponse['entries']:
        aLang = re.compile('(\w+)-').findall(aEntry['language'])
        if sLanguage and sLanguage not in aLang:
            continue
        elif sLanguage:
            aLang = [sLanguage]
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showHosters')
        oGuiElement.setTitle(aEntry['title'].encode('utf-8'))
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(URL_PROTOCOL + aEntry['cover'])
        oGuiElement.setYear(aEntry['year'])
        oGuiElement.setLanguage( ', '.join(map(str, aLang)))
        if oGui.isMetaOn:
            oGuiElement.addItemValue('imdb_id','tt'+aEntry['imdb'])
        oOutParms = ParameterHandler()
        oOutParms.setParam('itemID', aEntry['imdb'])
        oOutParms.setParam('lang', aEntry['language'])
        oGui.addFolder(oGuiElement, oOutParms, False, total, True)

    if int(oResponse['current']) < int(oResponse['pages']):
        params.setParam('page', int(oResponse['current']) + 1)
        oGui.addNextPage(SITE_IDENTIFIER, 'searchRequest', params)

    if not sGui:
        oGui.setView('movies')
        oGui.setEndOfDirectory()

def showHosters():
    params = ParameterHandler()
    imdbID = params.getValue('itemID')
    lang = params.getValue('lang')
    if not imdbID or not lang: return

    sLanguage = _getPrefLanguage()

    hosters = []
    for sLang in re.compile('(\w+)-').findall(lang):
        if sLanguage and sLanguage != sLang:
            continue

        oResponse = _getJSonResponse(URL_LINKS, {'ID':imdbID,'lang':sLang} )
        if 'links' not in oResponse or len(oResponse['links']) == 0:
            return

        for aEntry in oResponse['links']:
            hoster = dict()
            if oResponse['links'][aEntry][0].upper() in QUALITY_ENUM:
                hoster['quality'] = QUALITY_ENUM[oResponse['links'][aEntry][0]]
            hoster['link'] = URL_OUT % oResponse['links'][aEntry][1]
            hoster['name'] = aEntry
            hoster['displayedName'] = '%s (%s) - Quality: %s' % (aEntry.title(), sLang, oResponse['links'][aEntry][0])
            hosters.append(hoster)

    if hosters:
        hosters = sorted(hosters, key=lambda k: k['name']) #sort by hostername
        hosters.append('play')
    return hosters

def play(sUrl = False):
    if not sUrl: sUrl = oParams.getValue('url')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.request()
    sUrl = oRequestHandler.getRealUrl() # get real url from out-page

    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results

def _getJSonResponse(sUrl, parmDict):
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('X-Requested-With','XMLHttpRequest')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    for (prop, val) in parmDict.items():
        oRequest.addParameters(prop,val)
    return json.loads(oRequest.request())

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    dictSearch = SEARCH_DICT
    dictSearch['term'] = sSearchText.strip()
    searchRequest(dictSearch, oGui)

def _getPrefLanguage():
    sLanguage = cConfig().getSetting('prefLanguage')
    if sLanguage == '0':
        sLanguage = 'de'
    elif sLanguage == '1':
        sLanguage = 'en'
    else:
        sLanguage = False
    return sLanguage

def showYearSearch():
    oGui = cGui()
    dictSearch = SEARCH_DICT
    beginYear = correctWrongYearEntry(oGui.showNumpad(defaultNum=1913, numPadTitle="Begin Year"))
    endYear = correctWrongYearEntry(oGui.showNumpad(defaultNum=datetime.now().year, numPadTitle="End Year"))
    dictSearch['year[]'] = [beginYear, endYear]
    searchRequest(dictSearch, False)
    oGui.setEndOfDirectory()


def correctWrongYearEntry(year):
    if year == '' or int(year) < 1913:
        year = "1913"
    elif int(year) > datetime.now().year:
        year = datetime.now().year
    return year


def showRatingSearch():
    oGui = cGui()
    dictSearch = SEARCH_DICT
    minRating = oGui.showNumpad(defaultNum=1, numPadTitle="Min Rating")
    if int(minRating) > 9:
        minRating = "9"
    elif int(minRating) < 1:
        minRating = "1"
    dictSearch['rating'] = minRating
    searchRequest(dictSearch, False)
    oGui.setEndOfDirectory()
