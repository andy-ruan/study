#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' thread tools.
    author: andreruan@2013
'''
import Queue
import threading
import datetime

# thread pool to execute some process.
#   subclass should overwrite self.proc function.
class ThreadPool(object):
    def __init__(self, num, qlist, nameprefix="th"):
        self.thnum = max(num,1)
        self.name = nameprefix
        self.qlist = qlist
        self.stop_reason = ""
        self.stop_flag = False
        self.__suspend = threading.Event()
        self.__suspend_num = 1
        self.__suspend_lck = threading.RLock()
        self._tqueue = Queue.Queue()
        self._rqueue = Queue.Queue()
        self.resume()
        
    def resume(self):
        print '#'*10, "resume thread"
        self.__suspend.set()
        self.__suspend_timer = None
    
    def suspend(self, seconds = 60):        
        self.__suspend_lck.acquire()
        try:
            if not self.__suspend_timer:
                self.__suspend_num += 1
                self.__suspend.clear()
                seconds = int(seconds) * self.__suspend_num
                print '#'*10, "suspend thread", seconds, datetime.datetime.now()
                self.__suspend_timer = threading.Timer(seconds, self.resume)
                self.__suspend_timer.start()
        except:
            pass
        self.__suspend_lck.release()
    
    def proc(self, query, qsize):
        pass
        
    def put_data(self, query):
        self._tqueue.put_nowait(query)
        
    def run_and_wait(self):
        def thread_fun(tqueue, rqueue):
            while not self.stop_flag:
                self.__suspend.wait()
                try:
                    query = tqueue.get_nowait()
                except:
                    self.stop_reason = "no data"
                    self.stop_flag = True
                    break
                    
                ret = self.proc(query, tqueue.qsize())
                if ret:
                    rqueue.put_nowait(ret)
                tqueue.task_done()
                
        
        #tqueue = Queue.Queue()
        #rqueue = Queue.Queue()
        threads = []
        for l in self.qlist:
            self._tqueue.put_nowait(l)
        
        for i in xrange(self.thnum):
            threads.append(threading.Thread( \
                target = thread_fun,\
                name="%s-%s"%(self.name,i),\
                args=(self._tqueue, self._rqueue)))
        for t in threads:
            t.start()
        self._tqueue.join()
        
        rlist = []
        while self._rqueue.qsize():
            rlist.append(self._rqueue.get_nowait())
        return rlist

    __call__ = run_and_wait
############################################################   