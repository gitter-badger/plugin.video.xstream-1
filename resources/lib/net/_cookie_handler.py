import mechanize
import os, sys

from resources.lib import common


class CookieHandler(mechanize.BaseHandler):
    ignore_discard = False
    ignore_expired = False

    def __init__(self):
        self._cookie_jar = mechanize.LWPCookieJar()
        self._cookie_file_path = ''
        self._set_cookie_file_path()
        self._load_cookies()

    def _set_cookie_file_path(self, cookie_file=None):
        if not cookie_file:
            profile_path = common.profilePath
            cookie_file = os.path.join(profile_path, 'cookies.txt')
        if not os.path.exists(cookie_file):
            file_handle = open(cookie_file, 'w')
            file_handle.write('#LWP-Cookies-2.0')
            file_handle.close()
        self._cookie_file_path = cookie_file

    def _load_cookies(self):
        self._cookie_jar.load(self._cookie_file_path, self.ignore_discard, self.ignore_expired)

    def _save_cookies(self):
        self._fix_cookie_time()
        self._cookie_jar.save(self._cookie_file_path, self.ignore_discard, self.ignore_expired)

    def _fix_cookie_time(self):
        for entry in self._cookie_jar:
            if entry.expires > sys.maxint:
                entry.expires = sys.maxint

    def add_cookie(self, cookie):
        self._cookie_jar.set_cookie(cookie)

    def get_cookies(self, domain=None, path=None, name=None):
        cookies = []

        for cookie in self._cookie_jar:
            if domain and cookie.domain != domain:
                continue
            if path and cookie.path != path:
                continue
            if name and cookie.name != name:
                continue
            cookies.append(cookie)

        return cookies

    def del_cookies(self, domain=None, path=None, name=None):
        cookies = self.get_cookies(domain, path, name)

        for cookie in cookies:
            self._cookie_jar.clear(cookie.domain, cookie.path, cookie.name)

        self._save_cookies()

    def get_cookie_file_path(self):
        return self._cookie_file_path

    # from kennethreitz module "requests"
    def create_cookie(self, name, value, **kwargs):
        """Make a cookie from underspecified parameters.
        By default, the pair of `name` and `value` will be set for the domain ''
        and sent on every request (this is sometimes called a "supercookie").
        """
        result = dict(
            version=0,
            name=name,
            value=value,
            port=None,
            domain='',
            path='/',
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={'HttpOnly': None},
            rfc2109=False, )

        badargs = set(kwargs) - set(result)
        if badargs:
            err = 'create_cookie() got unexpected keyword arguments: %s'
            raise TypeError(err % list(badargs))

        result.update(kwargs)
        result['port_specified'] = bool(result['port'])
        result['domain_specified'] = bool(result['domain'])
        result['domain_initial_dot'] = result['domain'].startswith('.')
        result['path_specified'] = bool(result['path'])

        return mechanize.Cookie(**result)

    def http_request(self, request):
        self._cookie_jar.add_cookie_header(request)
        return request

    def http_response(self, request, response):
        self._cookie_jar.extract_cookies(response, request)
        self._save_cookies()
        return response

    https_request = http_request
    https_response = http_response