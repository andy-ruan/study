#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' http resource downloader
    author: andreruan@2013
'''

import os
import time
import sys
import urllib2
import pdb

conf = dict(    
    proxy_idc = '10.151.130.150:10086', # idc    
    proxy_oa = '10.1.156.87:8080', # web-proxy 
 )

class HttpClient(object):
    def __init__(self, proxy_addr = None, timeout=30):
        self.timeout = timeout
        self.headers = {}
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9'
        
        if proxy_addr:
            proxy_handler = urllib2.ProxyHandler({'http' : 'http://%s' %proxy_addr})
        else:
            proxy_handler = urllib2.ProxyHandler({})
        self.opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
        if not hasattr(sys, 'version_info') or sys.version_info < (2, 6):
            import socket
            socket.setdefaulttimeout(timeout)
            self.timeout = 0
    def SetHeader(self, key, val):
        self.headers[key] = val

    def TryGet(self, url):
        request = urllib2.Request(url)
        for k,v in self.headers.items():
            if v:
                request.add_header(k, v)
        #print "TryGet", url
        try:
            if self.timeout > 0:
                resp = self.opener.open(request, timeout=self.timeout)
            else:
                resp = self.opener.open(request)
            return resp
        except urllib2.HTTPError, e:
            return e.code
        except:
            return None

class HttpSpider(HttpClient):
    def Crawl(self, url, trycnt = 5):
        for i  in xrange(trycnt):
            try:
                resp = self.TryGet(url)
                if isinstance(resp, int):
                    print resp
                    return None
                htm = resp.read()
                return htm
            except Exception, e:
                pass
        return None
        
    def DeadlinkDetect(self, url, trycnt = 5):
        for i in xrange(trycnt):
            try:
                resp = self.TryGet(url)
                if resp == 404:
                    return True
                htm = resp.read()
                if len(htm):
                    return False
            except Exception, e:
                pass
        return False    


if __name__ == '__main__':
    url = "http://t3.baidu.com/it/u=4164897210,2454560004&fm=20"
    url = "http://t1.baidu.com/it/u=1097663962,583554527&fm=20"
    d = HttpSpider(timeout=5, proxy_addr=conf["proxy_idc"])
    d.SetHeader('Referer', 'http://video.baidu.com/')
    print d.Crawl(url)


