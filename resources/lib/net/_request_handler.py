import httplib
import mechanize
import urllib
import xbmcgui

from _cache_helper import CacheHelper
from _cookie_handler import CookieHandler
from _http_handler import HTTPSHandler
from _cloudflare_processor import CloudFlareProcessor
from _response import xResponse

from resources.lib import logger

USERAGENT_FIREFOX = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'


class RequestHandler(object):
    _headers = None
    _parameters = None
    _response = None
    _timestamp = None
    _type = None
    _cookie_handler = CookieHandler()

    def __init__(self, url, use_cache=True, ignore_errors=True, compression=True):
        self._url = url.replace(' ', '+')
        self._use_cache = use_cache
        self._ignore_errors = ignore_errors
        self._compression = compression
        self.set_useragent(USERAGENT_FIREFOX)

        # XXX Only call it once on init to be sure that the chache doesn't get deleted between a has_cache() call and
        # the actual request
        if use_cache:
            CacheHelper.clean_cache()

    def add_header(self, key, value):
        if not self._headers:
            self._headers = {}

        self._headers[key] = value

    def get_headers(self):
        return self._headers

    def del_header(self, key):
        if key in self._headers:
            del self._headers[key]

    def add_parameter(self, key, value, quote=False):
        if not self._parameters:
            self._parameters = {}

        if not quote:
            self._parameters[key] = value
        else:
            self._parameters[key] = urllib.quote(str(value))

    def get_parameter(self):
        return self._parameters

    def del_parameter(self, key):
        if key in self._parameters:
            del self._parameters[key]

    def set_useragent(self, useragent):
        self.add_header('User-agent', useragent)

    def set_request_type(self, type):
        if not type in ['GET', 'POST']:
            raise ValueError('Invalid request type')
        self._type = type

    def _build_opener(self):
        handlers = [
            self.cookies,
            HTTPSHandler(),
            CloudFlareProcessor()
        ]

        return mechanize.build_opener(*handlers)

    def _build_request(self):
        request = mechanize.Request(self._url)

        if self._parameters:
            parameters = urllib.urlencode(self._parameters, True)

            if self._type == 'GET':
                request = mechanize.Request('%s?%s' % (self._url, parameters))
            else:
                request = mechanize.Request(self._url, parameters)

        if self._headers:
            for key in self._headers:
                request.add_header(key, self._headers[key])

        if self._compression:
            request.add_header('Accept-Encoding', 'gzip')

        return request

    @property
    def url(self):
        return self._url

    @property
    def cookies(self):
        return self._cookie_handler

    @property
    def response(self):
        return self._response

    def has_cache(self):
        return CacheHelper.has_cache(self._url)

    def request(self):
        request = self._build_request()
        opener = self._build_opener()

        ch = None
        if self._use_cache:
            ch = CacheHelper(request.get_full_url())
            cache = ch.load_chache()

            if cache:
                return cache

        response = None
        try:
            print 'DUrl: %s' % request.get_full_url()
            response = opener.open(request)
        except mechanize.HTTPError, e:
            if not self._ignore_errors:
                xbmcgui.Dialog().ok('xStream', 'Fehler beim Abrufen der Url:', self._url, str(e))
                logger.error("HTTPError " + str(e) + " Url: " + self._url)
            else:
                response = e
        except mechanize.URLError, e:
            xbmcgui.Dialog().ok('xStream', str(e.reason), 'Fehler')
            logger.error("URLError " + str(e.reason) + " Url: " + self._url)
        except httplib.HTTPException, e:
            xbmcgui.Dialog().ok('xStream', str(e))
            logger.error("HTTPException " + str(e) + " Url: " + self._url)

        if not response:
            return None

        resp = xResponse(response)

        if self._use_cache:
            ch.save_cache(resp)

        return resp

    @classmethod
    def urlopen(cls, url, use_cache=True):
        rh = cls(url, use_cache)
        return rh.request()