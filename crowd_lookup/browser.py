# -*- coding: utf-8 -*-

import re, json
import time
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class Browser:
    def __init__(self):
        self._br = mechanize.Browser()
        self._set_cookie_jar()
        self._set_options()
        self._cur_gag = -1

    def _set_cookie_jar(self):
        cj = cookielib.LWPCookieJar()
        self._br.set_cookiejar(cj)

    def _set_options(self):
        self._br.set_handle_equiv(True)
        self._br.set_handle_redirect(True)
        self._br.set_handle_referer(True)
        self._br.set_handle_robots(False)
        self._br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self._br.addheaders = [('User-agent', 
                                '''Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) 
                                Gecko/2008071615 
                                Fedora/3.0.1-1.fc9 
                                Firefox/3.0.1''')]

    def _remove_script_tag(self, src):
        dst = ''
        while src != '':
            pos = src.find('<script')
            if pos == -1:
                dst += src
                break
            else:
                dst += src[: pos]
                pos = src.find('</script>')
                src = src[pos + len('</script>') :]
        return dst

    def query_dict(self, word):
        word = word.lower()
        return '配備, 裝備'
        #self._url = 'http://dict.dreye.com/ews/dict.php?w=%s&hidden_codepage=01&ua=dc_cont&project=nd' % word
        #page = self._br.open(self._url)
        #content = page.read()
        #content = re.sub('/ >', '/>', content) # workaround for strange BeautifulSoup...
        #content = self._remove_script_tag(content)
        #self._soup = BeautifulSoup(content)
        #try:
        #    defi = self._soup.find('div', {'id': 'infotab1'}) \
        #                     .find('div', {'class': 'dict_cont'})
        #    defi = ' '.join([str(ins) for ins in defi])
        #except:
        #    raise
        #return defi

if __name__ == '__main__':
    br = Browser()
    print br.query_dict('cool')

