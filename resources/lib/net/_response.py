import gzip
import StringIO
import re


class xResponse(object):
    remove_new_lines = True
    remove_break_lines = True

    def __init__(self, response):
        self._headers = response.info()
        self._url = response.geturl()
        self._code = response.code
        self._msg = response.msg
        self._parse_html(response)

    # from eldorados module "urlresolver"
    def _parse_html(self, response):
        html = response.read()
        response.close()

        try:
            if self._headers['content-encoding'].lower() == 'gzip':
                html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
        except:
            pass

        try:
            content_type = self._headers['content-type']
            if 'charset=' in content_type:
                encoding = content_type.split('charset=')[-1]
        except:
            pass

        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);\s+charset=(.+?)"', html, re.IGNORECASE)
        if r: encoding = r.group(1)
        try:
            html = unicode(html, encoding)
        except:
            pass

        self._content = html

    def info(self):
        return self._headers

    def geturl(self):
        return self._url

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg

    @property
    def content(self):
        content = self._content
        if self.remove_new_lines:
            content = content.replace("\n", "")
            content = content.replace("\r\t", "")

        if self.remove_break_lines:
            content = content.replace("&nbsp;", "")
        return content
