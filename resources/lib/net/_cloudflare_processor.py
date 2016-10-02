#!/usr/bin/env python2.7
from time import sleep
import mechanize
import urllib
import re

from urlparse import urlparse


class CloudFlareProcessor(mechanize.HTTPErrorProcessor):
    def http_error_503(self, req, fp, code, msg, hdrs):
        print 'CloudFlare 2'
        if hdrs.get("Server") == 'cloudflare-nginx':
            sleep(5)

            useragent = req.headers.get('User-agent')

            body = fp.read()
            parsed_url = urlparse(fp.geturl())
            submit_url = "%s://%s/cdn-cgi/l/chk_jschl" % (parsed_url.scheme, parsed_url.netloc)

            params = {}

            try:
                params["jschl_vc"] = re.search(r'name="jschl_vc" value="(\w+)"', body).group(1)
                params["pass"] = re.search(r'name="pass" value="(.+?)"', body).group(1)

                js = self._extract_js(body)
            except:
                raise

            params["jschl_answer"] = str(js + len(parsed_url.netloc))

            sParameters = urllib.urlencode(params, True)

            request = mechanize.Request("%s?%s" % (submit_url, sParameters))
            request.add_header('Referer', fp.geturl())
            request.add_header('User-agent', useragent)

            fp.close()

            return self.parent.open(request)


    def _extract_js(self, body):
        js = re.search(r"setTimeout\(function\(\){\s+(var "
                           "s,t,o,p,b,r,e,a,k,i,n,g,f.+?\r?\n[\s\S]+?a\.value =.+?)\r?\n", body).group(1)
        js = re.sub(r"a\.value = (parseInt\(.+?\)).+", r"\1", js)
        js = re.sub(r"\s{3,}[a-z](?: = |\.).+", "", js)

        # Strip characters that could be used to exit the string context
        # These characters are not currently used in Cloudflare's arithmetic snippet
        js = re.sub(r"[\n\\']", "", js)

        varname = re.search(", (.*)=\{", js).group(1)
        varname += "."
        varname += re.search("\"(.*)\"", js).group(1)

        result = re.findall(varname + "(.*?);", js)
        result.insert(0, "+=" + re.search(":(.*)}", js).group(1))

        val = 0

        for item in result:
            if item[0] == '+':
                val += self._decode(item[2:])
            elif item[0] == '-':
                val -= self._decode(item[2:])
            elif item[0] == '*':
                val *= self._decode(item[2:])
            elif item[0] == '/':
                val /= self._decode(item[2:])

        return val

    def _decode(self, inp):
        sign = '+'
        if inp[0] == '+' or inp[0] == '-':
            sign = inp[0]
            inp = inp[1:]

        inp = inp.replace("![]", "False")
        inp = inp.replace("[]", "False")

        while "!True" in inp or "!False" in inp:
            inp = inp.replace("!True", "False")
            inp = inp.replace("!False", "True")

        inp = inp.replace("!+True", "False")
        inp = inp.replace("!+False", "True")
        inp = inp.replace("(", "str(")

        number = int(eval(inp))

        if sign == '-':
            number = -number

        return number

    def createUrl(self, sUrl, oRequest):
        parsed_url = urlparse(sUrl)

        netloc = parsed_url.netloc[4:] if parsed_url.netloc.startswith('www.') else parsed_url.netloc

        cfId = oRequest.getCookie('__cfduid', '.'+ netloc)
        cfClear = oRequest.getCookie('cf_clearance', '.'+ netloc)

        if cfId and cfClear and 'Cookie=Cookie:' not in sUrl:
            delimiter = '&' if '|' in sUrl else '|'
            sUrl = sUrl + delimiter + "Cookie=Cookie: __cfduid=" + cfId.value + "; cf_clearance=" + cfClear.value

        if 'User-Agent=' not in sUrl:
            delimiter = '&' if '|' in sUrl else '|'
            sUrl += delimiter + "User-Agent=" + oRequest.getHeaderEntry('User-Agent')

        return sUrl

    https_error_503 = http_error_503