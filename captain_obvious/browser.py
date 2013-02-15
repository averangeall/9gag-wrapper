# -*- coding: utf-8 -*-

import re, json
import time
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class Browser:
    OKAY = 'OKAY'
    NSFW = 'NSFW'
    REMOVED = 'REMOVED'
    NOT_FOUND = 'NOT_FOUND'
    HTML_MALFORMED = 'HTML_MALFORMED'
    VIDEO = 'VIDEO'

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

    def _read_graph_api(self, url):
        okay = False
        while not okay:
            try:
                page = self._br.open(url)
                okay = True
            except:
                time.sleep(1)
        content = page.read()
        return json.loads(content)

    def _reverse_html_escape(self, string):
        pairs = [('&', '&amp;'),
                 ('<', '&lt;'),
                 ('>', '&gt;'),
                 ('"', '&quot;'),
                 ("'", '&#0*39;'),
        ]
        for pair in pairs:
            string = re.sub(pair[1], pair[0], string)
        return string

    def open_gag(self, gid):
        if self._cur_gag == gid:
            return

        self._url = 'http://9gag.com/gag/%d' % gid
        try:
            page = self._br.open(self._url)
            self._cur_gag = gid
        except KeyboardInterrupt:
            raise 
        except:
            return Browser.NOT_FOUND

        content = page.read()
        content = re.sub('/ >', '/>', content) # workaround for strange BeautifulSoup...
        content = re.sub('nsfw-post"', 'nsfw-post', content) # workaround for strange 9gag html...
        try:
            self._soup = BeautifulSoup(content)
        except:
            return Browser.HTML_MALFORMED

        if self._soup.find('p', {'class': 'form-message error '}) is not None:
            return Browser.REMOVED

        if self._soup.find('div', {'class': 'post-info-pad'}) is None:
            return Browser.NSFW

        if self._soup.find('div', {'class': 'video-post'}) is not None:
            return Browser.VIDEO

        return Browser.OKAY

    def get_title(self):
        info_pad = self._soup.find('div', {'class': 'post-info-pad'})
        title = info_pad.find('h1').string
        title = unicode(title)
        return self._reverse_html_escape(title)

    def get_image_url(self):
        image_url = 'http:' + self._soup.find('div', {'class': 'img-wrap'}).find('img')['src']
        return image_url

    def get_fb_profile(self, uid):
        profile = self._read_graph_api('https://graph.facebook.com/fql?q=SELECT+url+FROM+profile_pic+WHERE+id=%s' % uid)
        return profile['data'][0]['url']

    def get_fb_name(self, uid):
        name = self._read_graph_api('https://graph.facebook.com/fql?q=SELECT+name+FROM+profile+WHERE+id=%s' % uid)
        return name['data'][0]['name']

    def get_comments(self):
        raw_streams = self._read_graph_api('https://graph.facebook.com/comments/?ids=%s&limit=1000' % self._url)

        parsed_streams = []
        for raw_stream in raw_streams[self._url]['comments']['data']:
            parsed_stream = []
            parsed_stream.append({'cid': raw_stream['id'],
                                  'uid': raw_stream['from']['id'],
                                  'content': raw_stream['message'],
                                  'num_like': int(raw_stream['like_count'])
                                 })
            if 'comments' in raw_stream:
                for raw_reply in raw_stream['comments']['data']:
                    parsed_stream.append({'cid': raw_reply['id'],
                                          'uid': raw_reply['from']['id'],
                                          'content': raw_reply['message'],
                                          'num_like': -1
                                         })
            parsed_streams.append(parsed_stream)

        return parsed_streams


