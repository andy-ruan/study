#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' thread tools.
    author: andreruan@2013
'''
import Queue
import threading

import time

# thread pool to execute some process.
#   subclass should overwrite self.proc function.
class ThreadPool(object):
    def __init__(self, num, qlist, nameprefix="th"):
        self._thnum = max(num,1)
        self._name = nameprefix
        self._qlist = qlist
        self._lock = threading.Lock()
        self._tqueue = Queue.Queue()
        self._rqueue = Queue.Queue()
        self._threads = []
    
    def proc(self, query, qsize):
        pass
        
    def run(self):
        def thread_fun(tqueue, rqueue):
            while tqueue.qsize() > 0:
                try:
                    query = tqueue.get_nowait()
                    ret = self.proc(query, tqueue.qsize())
                except Queue.Empty:
                    break
                except:
                    ret = None
                    
                if ret:
                    rqueue.put_nowait(ret)
        
        for l in self._qlist:
            self._tqueue.put_nowait(l)
        
        for i in xrange(self._thnum):
            self._threads.append(threading.Thread( \
                target = thread_fun,\
                name="%s-%s"%(self._name,i),\
                args=(self._tqueue, self._rqueue)))
        for t in self._threads:
            t.start()
            
    def run_and_wait(self):
        self.run()
        return self.get_result()
        
    def get_result(self):
        for t in self._threads:
            t.join()
        return self._queue_to_list(self._rqueue)

    def _queue_to_list(self, queue):
        result = []
        while queue.qsize():
            result.append(queue.get_nowait())
        return result

    __call__ = run_and_wait
############################################################   

# base class for thread.
class MultiThreadMix(threading.Thread):
    def __init__(self, duration = 0, idx = 0, name="Thread"):
        self.idx = idx
        threading.Thread.__init__(self, name="%s-%d"%(name,idx))
        self.in_queue = None
        self.ou_queue = None
        self.stop_flag = False
        if duration and duration > 0:
            self.duration = duration * 0.000001
        else:
            self.duration = 0
        print self.duration
        
    def set_queue(self, in_queue, ou_queue = None):
        self.in_queue = in_queue
        self.ou_queue = ou_queue
                
    def set_stop(self): self.stop_flag = True
        
    def proc(self, data, qsize):
        self.in_queue.task_down()
        return True
        
    def after_done(self):
        pass
        
    def prev_exec(self):
        pass
        
    def post_exec(self):
        pass
        
    def run(self):
        idx = 0
        self.prev_exec()
        
        while True:
            ret = None
            try:
                data = self.in_queue.get(timeout = 2)
                idx = 0
                ret = self.proc(data, self.in_queue.qsize())
            except Queue.Empty:
                if idx >= 5 and self.stop_flag:
                    break
                idx += 1
                time.sleep(0.1)
            except:
                ret = None
                
            if ret and self.ou_queue:
                self.ou_queue.put(ret)

            if self.duration > 0:
                time.sleep(self.duration)
                
        self.after_done()
        self.post_exec()

# threading._Timer triger only ONCE and EXIT.
class Timer(threading.Thread):
    def __init__(self, interval, function, *args, **kwargs):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                break
            self.function(*self.args, **self.kwargs)

# threading._Semaphore
# Semaphore whose bound can be modified.
class Semaphore(object):
    # After Tim Peters' semaphore class, but not quite the same (no maximum)
    def __init__(self, value=1):
        if value < 0:
            raise threading.ValueError("semaphore initial value must be >= 0")
        self.__cond = threading.Condition(threading.Lock())
        self.__value = value

    def acquire(self, blocking=1):
        rc = False
        self.__cond.acquire()
        while self.__value == 0:
            if not blocking:
                break
            self.__cond.wait()
        else:
            self.__value = self.__value - 1
            rc = True
        self.__cond.release()
        return rc

    __enter__ = acquire

    def release(self):
        self.__cond.acquire()
        self.__value = self.__value + 1
        self.__cond.notify()
        self.__cond.release()

    def __exit__(self, t, v, tb):
        self.release()
    
    # different from threading._Semaphore
    def set_value(self, value):
        self.__cond.acquire()
        self.__value = value
        self.__cond.notify()
        self.__cond.release()
            
def __test_timer():
    import datetime
    def Hello(msg):
        now = datetime.datetime.now()
        print "Hello ", msg, now

    a = Timer(1.5, Hello, "nihao")
    a.start()
    time.sleep(10)
    a.cancel()
    Hello(msg="Hi")
    a.join()
    
if __name__ == '__main__':
   __test_timer()
