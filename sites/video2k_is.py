# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'video2k_is'
SITE_NAME = 'Video2k'
SITE_ICON = 'video2k.png'

URL_MAIN = 'http://www.video2k.is/'
URL_MOVIE = URL_MAIN + '?c=movie&m=filter&order_by=%s'
URL_GENRE = URL_MAIN + '?c=movie&m=filter&genre=%s'
URL_SEARCH = URL_MAIN + '?keyword=%s&c=movie&m=filter'
URL_Hoster = URL_MAIN + '?c=ajax&m=movieStreams2&id=%s'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl',URL_MOVIE % 'releases')
    oGui.addFolder(cGuiElement('Neu', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_MOVIE % 'featured')
    oGui.addFolder(cGuiElement('Kino', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_MOVIE % 'views')
    oGui.addFolder(cGuiElement('Top', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_MOVIE % 'updates')
    oGui.addFolder(cGuiElement('Updates', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'))
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showGenre():
    oGui = cGui()
    params = ParameterHandler()
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    parser = cParser()
    isMatch, sHtmlContainer = parser.parseSingleResult(sHtmlContent, 'Genre</option>[^>].*?</select>')

    if not isMatch: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    isMatch, aResult = parser.parse(sHtmlContainer, "<option[^>]*value='([^']*)'[^>]*>([^<]+)</option>")

    if not isMatch: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    for sValue, sTitle in aResult:
        params.setParam('sUrl', URL_GENRE % sValue)
        oGui.addFolder(cGuiElement(sTitle, SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()  

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')

    oRequestHandler = cRequestHandler(entryUrl)
    oRequestHandler.addHeaderEntry('Referer', entryUrl)
    sHtmlContent = oRequestHandler.request()

    parser = cParser()
    pattern = '<li[^>]*title="(.*?)\((:?\d+)?\).*?(:?\s+-\s+(:?[^"]+))?"[^>]*>.*?' # name / year / desc
    pattern += "<a[^>]*href='[^>]*-(\d+).[^>]*'[^>]*>.*?" # url
    pattern += "<img[^>]*src='([^']*)'[^>]*>.*?" # img
    pattern += "</li>" # title
    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (aResult)
    for sName, sYear, sUglyDesc, sDesc, sUrl, sThumbnail in aResult:
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setDescription(cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8'))
            oGuiElement.setYear(sYear)
            params.setParam('sUrl', URL_Hoster % sUrl)
            oGui.addFolder(oGuiElement, params, False, total)

    isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, '</strong>.*?<a[^>]*href="([^"]+)"[^>]*>\d+')
    if isMatchNextPage:
        params.setParam('sUrl', URL_MAIN + cUtil().unescape(sNextUrl))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if not sGui:
        oGui.setEndOfDirectory()

def showHosters():
    sUrl = ParameterHandler().getValue('sUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    sPattern = "<a[^>]*href='([^']+)'(:?[^>]*player.*?, \"([^\"]+)\")?.*?<span[^>]*class='?url'?[^>]*>(.*?)</span>"
    isMatch, aResult = cParser().parse(sHtmlContent, sPattern)

    hosters = []
    if isMatch:
        for sHref, sUglyEmbeded, sEmbeded, sName in aResult:
            hoster = {}
            hoster['link'] = (sHref if sHref != '#player' else sEmbeded)
            hoster['name'] = sName
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def getHosterUrl(sUrl = False):
    if not sUrl: sUrl = ParameterHandler().getValue('sUrl')
    
    if URL_MAIN in sUrl:
        sUrl = _redirectHoster(sUrl)

    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results

def _redirectHoster(url):
    # WHY?! Why is this not working? :'(
    #oRequestHandler = cRequestHandler(url)
    #oRequestHandler.addHeaderEntry('Referer', url)
    #oRequestHandler.request()
    #return oRequestHandler.getRealUrl()

    import urllib2
    opener = urllib2.build_opener()
    opener.addheaders = [('Referer', url)]
    try:
        resp = opener.open(url)
        if url != resp.geturl():
            return resp.geturl()
        else:
            return url
    except urllib2.HTTPError, e:
        if e.code == 403:
            if url != e.geturl():
                return e.geturl()
        raise ResolverError('File not found')

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH % sSearchText.strip(), oGui)
