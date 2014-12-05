#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' cgi base tools.
    author: andreruan@2012
'''

import sys
import json
import os
import os.path
import cgi

import log_base as exp

############################################################

def init_cgi():
    print 'Content-Type: text/html; charset=UTF-8\n'
    print '\n'
 
# parse CGI request parameters. k1=v1&k2=v2
def getQueryDict(query_string):
    query_dict = {}
    for each in query_string.split("&"):
        vals = each.split("=")
        key,val = "", ""
        for i in range(len(vals)):
            if len(key) > 0:
                break
            key += vals[i]
        if len(key) >= 1:
            query_dict[key] = "=".join(vals[i:])
    return query_dict

def getQueryDictNoCase(query_string):
    query_dict = getQueryDict(query_string)
    ret_dict = {}
    for key, val in query_dict.iteritems():
        ret_dict[key.lower()] = val
    return ret_dict
   
class XCGIEntity(object):
    ''' CGI请求处理动作的实体, 从此类派生出自己的动作处理类.        
    '''
    def __init__(self, logger):
        self.logger = logger
        
    def set_debug(self, flag):
        self.debug = flag
        
    def _dispatch(self, queryDict):
        try:
            fun = getattr(self, self.method)
        except:
            return 210, "not support %s"%(self.method)
            
        try:
            return fun(queryDict)
        except Exception,e:
            stack = exp.get_exception_stack()
            return 220, "%s\n\n%s"%(str(e),stack)
            
    def do_work(self, queryDict):
        self.method =  queryDict.get("method", None)
        if self.method:
            return self._dispatch(queryDict)
        elif hasattr(self, "list_methods"):
            msg = self.list_methods()
            return 0, msg.replace("\n","<br/>").replace(" ", "&nbsp;")
        else:
            return 200, "need method"

class XCGIEntry(object):
    ''' CGI程序入口, 使用方法:
        logger = get_logger(...)
        init_cgi()
        entity = XCGIEntity(logger)
        entry = XCGIEntry(logger, entity)
        entry.do_Main()
    '''
    def __init__(self, logger, entity):
        self.queryDict = {}
        self.logger = logger
        self.debug = False
        self.agent = entity

    def do_Main(self):
        code, msg = 100, ""
        try:
            code, msg = self.do_CGIRequest()
        except Exception,e:
            stack = exp.get_exception_stack()
            msg = "%s\n\n%s\n\n%s\n"%(str(e), "#"*100, stack)
            msg = msg.replace("\n","<br/>")
        
        self.do_CGIResponse(code, msg)
            
    def do_CGIRequest(self):
        method = os.environ.get("REQUEST_METHOD",None)
        queryString = os.environ.get("QUERY_STRING", "")
        self.queryDict = getQueryDictNoCase(queryString)
        code = 110
        if not queryString:
            msg = u"need queryString"
        if method not in ("GET", "POST"):
            msg = u"should be GET or POST, not %s"%method
        elif method == 'GET':   # do_GET
            self.debug = self.queryDict.get("debug", False)
            self.agent.set_debug(self.debug)
            self.logger.info("query: %s"%(str(self.queryDict)))
            code, msg = self.agent.do_work(self.queryDict)
        else:                   # do_POST
            postStr = sys.stdin.read()
            self.queryDict.update(json.loads(postStr))
            self.logger.info("query: %s"%(str(self.queryDict)))
            code, msg = self.agent.do_work(self.queryDict)
        return code, msg
        
    def do_CGIResponse(self, code, message):
        print "<html><head><title></title></head>"
        print "<style>"
        print "tr:nth-child(even) { /*COLOR: black; LINE-HEIGHT: 10pt; */ BACKGROUND-COLOR: #e3e2ed }"
        print "tr:nth-child(odd){ /*COLOR: black; LINE-HEIGHT: 10pt; */ BACKGROUND-COLOR: #fff }"
        print "</style>"
        print "<body>"
        if self.debug:
            print "request: "
            print str(self.queryDict)
            print "<br/>" * 2
        print "code: "
        print code
        print "<br/>"
        print unicode(message).encode("utf-8")
        print "<br/>" * 2
        print "</body></html>"
############################################################
