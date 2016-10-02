#!/usr/bin/env python2.7
import urllib

from resources.lib.net import RequestHandler
from resources.lib.net._cache_helper import CacheHelper


class cRequestHandler:
    def __init__(self, sUrl, caching=True, ignoreErrors=False):
        self._request = RequestHandler(sUrl, caching, ignoreErrors)
        self._response = None
        self.ignoreDiscard(False)
        self.ignoreExpired(False)
        self.removeBreakLines(True)
        self.removeNewLines(True)

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def setRequestType(self, cType):
        self._request.set_request_type(cType)

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        self._request.add_header(sHeaderKey, sHeaderValue)

    def getHeaderEntry(self, sHeaderKey):
        headers = self._request.get_headers()
        if sHeaderKey in headers:
            return headers[sHeaderKey]

    def addParameters(self, key, value, quote=False):
        self._request.add_parameter(key, value)

    def getResponseHeader(self):
        if self._response:
            self._response.info()
        return None

    # url after redirects
    def getRealUrl(self):
        if self._response:
            return self._response.geturl()
        return None

    def request(self):
        self._response = self._request.request()

        if self._response:
            self._response.remove_new_lines = self.__bRemoveNewLines
            self._response.remove_break_lines = self.__bRemoveBreakLines
            return self._response.content

        return ''

    def getRequestUri(self):
        params = self._request.get_parameter()
        parameters = ''
        if params:
            parameters = urllib.urlencode(params)
        return self._request.url + '?' + parameters

    # same as getRealUrl() ???
    def getHeaderLocationUrl(self):
        if self._response:
            return self._response.geturl()
        return None

    def createCookie(self, name, value, **kwargs):
        return self._request.cookies.create_cookie(name, value, **kwargs)

    def getCookie(self, sCookieName, sDomain=None):
        return self._request.cookies.get_cookies(sDomain, name=sCookieName)[0]

    def setCookie(self, oCookie):
        self._request.cookies.add_cookie(oCookie)

    def ignoreDiscard(self, bIgnoreDiscard):
        self._request.cookies.ignore_discard = bIgnoreDiscard

    def ignoreExpired(self, bIgnoreExpired):
        self._request.cookies.ignore_expired = bIgnoreExpired

    def clearCache(self):
        CacheHelper.clean_cache()