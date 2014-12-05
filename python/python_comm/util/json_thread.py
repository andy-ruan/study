#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' json interface in thread.
    author: andreruan@2013
'''

import os
import threading
import json as JSON

class JsonInThread(object):
    def __init__(self):
        self.lock = threading.Lock()

    def _call_in_thread(self, func, *args, **kwargs):
        self.lock.acquire()
        try:
            exp = None
            ret = func(*args, **kwargs)
        except Exception,e:
            exp = e
        self.lock.release()
        if exp:
            raise exp
        return ret


    def dumps(self, *args, **kwargs):
        return self._call_in_thread(JSON.dumps, *args, **kwargs)

    def loads(self, *args, **kwargs):
        return self._call_in_thread(JSON.loads, *args, **kwargs)

json = JsonInThread()

if __name__ == "__main__":
    import sys
    import random
    lock = threading.Lock()
    def func():
        for i in xrange(100):
            name = threading.currentThread().getName()
            val = random.random()
            try:
                if i % 2 == 0:
                    tmp = {"int":"12345", "str":"hello"}
                    res = json.dumps(tmp)
                    ret2 = JSON.dumps(tmp)
                else:
                    tmp = '{ "int" :"12345", "str":"hello" }'
                    res = json.loads(tmp)
                    ret2 = JSON.loads(tmp)
                lock.acquire()
                print name, type(tmp), type(res), type(ret2)
                lock.release()
            except Exception,e:
                print name, e
        return
    threads = []
    for i in xrange(10):
        th = threading.Thread( name="thread-%s"%i, target = func)
        threads.append(th)

    for th in threads: th.start()
    for th in threads: th.join()
