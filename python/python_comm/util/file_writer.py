#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' file writer.
    author: andreruan@2013
'''

import os
import datetime
import threading
           
class FileWriter(object):
    def __init__(self, prefix, rotate_cnt = 0):
        #  self.turn, self.count, self.fp
        self.count = 0
        self.turn = 0
        self.lock = threading.Lock()

        if rotate_cnt:
            self.rotate_cnt = int(rotate_cnt)
        else:
            self.rotate_cnt = 0
            
        self.prefix = prefix
        self.fp = None
        if self.rotate_cnt <= 0:
            self.write = self._write_no_rotate
        else:
            self._load_turn()
            self.write = self._write_rotate

    def open(self):
        if self.fp:
            return

        if self.rotate_cnt <= 0:
            filename = self.prefix
            self.fp = open(filename, "w")
        else:
            filename = "%s.%s.tmp"%(self.prefix, self.turn)
            self.fp = open(filename, "a")

    def close(self):
        if self.fp and self.count > 0 and self.rotate_cnt > 0:
            self._save_tmp_file()
        elif self.fp:
            self.fp.close()
    
    def _write_msg(self, msg):
        self.fp.write(msg)
        self.fp.flush()
        #os.fsync(self.fp) 
        self.count += 1

    def _write_no_rotate(self, msg):
        self.lock.acquire()
        try:
            self._write_msg(msg)
        except Exception, e:
            print "_write_no_rotate", e
        self.lock.release()
    

    def _write_rotate(self, msg):
        self.lock.acquire()
        try:
            if self.count >= self.rotate_cnt:
                self._save_tmp_file()
                self.turn += 1
                self._save_turn()
            self.open()
            self._write_msg(msg)
        except Exception, e:
            print "_write_rotate", e
        self.lock.release()

    def _save_tmp_file(self):
        dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        tmp_name = "%s.%s.tmp"%(self.prefix, self.turn)
        dst_name = "%s.%s.%s.rdy"%(self.prefix, self.turn, dt)
        self.fp.close()
        os.rename(tmp_name, dst_name)
        self.fp = None
        self.count = 0

    def save_tmp_file(self):
        if self.count == 0:
            return False
        self.lock.acquire()
        try:
            print self.turn, self.count
            self._save_tmp_file()
            self.open()
        except Exception, e:
            print 'save_tmp_file', e
            raise e
        self.lock.release()
        return True
        
    def _load_turn(self):
        filename = "%s.TURN_COUNT"%(self.prefix)
        try:
            val = open(filename).read()
            self.turn = int(val.strip())
        except:
            self.turn = 0
            
    def _save_turn(self):
        filename = "%s.TURN_COUNT"%(self.prefix)
        fp = open(filename, "w")
        fp.write("%s"%(self.turn))
        fp.close()
  
class FileWriterInThread(object):
    def __init__(self, prefix, rotate_cnt = 0):
        self.lock = threading.Lock()
        self.writer = FileWriter(prefix, rotate_cnt)

    def open(self): self.writer.open()
    def close(self): self.writer.close()
    
    def write(self, msg):
        self.lock.acquire()
        try:
            self.writer.write(msg)
            exp = None
        except Exception, e:
            exp = e
            
        self.lock.release()
        if exp: raise exp

if __name__ == "__main__":
    fp = FileWriter("./test.txt", 100)
    fp_2 = FileWriter("./test2.txt")
    fp.open()
    fp_2.open()
    for i in range(113):
        fp.write(str(i)+"\n")
        fp_2.write(str(i)+"\n")
        if i % 11 == 0:
            fp.save_tmp_file()
    fp.close()
    fp_2.close()
