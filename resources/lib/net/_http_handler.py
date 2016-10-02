import httplib
import socket
import sys

import mechanize


class HTTPSHandler(mechanize.HTTPSHandler):
    def http_open(self, req):
        if (2, 7, 9) <= sys.version_info < (2, 7, 11):
            conn_factory = HTTPSConnection
        else:
            conn_factory = httplib.HTTPSConnection

        return mechanize.HTTPSHandler.do_open(self, conn_factory, req)


class HTTPSConnection(httplib.HTTPSConnection):
    def __init__(self, host, port=None, key_file=None, cert_file=None, strict=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, context=None):
        import ssl
        context = ssl._create_unverified_context()
        httplib.HTTPSConnection.__init__(self, host, port, key_file, cert_file, strict, timeout, source_address, context)
