#!/usr/bin/env python
# -*-: coding: gbk -*-

import sys
import threading

class IDSet(object):
    def __init__(self, filename = "idset.txt"):
        self.lock = threading.Lock()
        self.idset = set([])
        self.filename = filename

    def size(self): return len(self.idset)

    def loads(self, filename = None):
        if not filename:
            filename = self.filename
        fp = open(filename, "r")
        for line in fp:
            line = line.strip()
            if len(line) <= 2:
                continue
            if line[0] == "#":
                continue
            self.idset.add(line)
        fp.close()
        
    def dumps(self, filename = None):
        if not filename:
            filename = self.filename
        lines = [ x+"\n" for x  in self.idset]
        lines.sort()
        file(filename, "w").writelines(lines)
        
    def check(self, id):
        strid = str(id)
        self.lock.acquire()
        ret = strid in self.idset
        self.lock.release()
        return ret
        
    def check_and_add(self, id):
        strid = str(id)
        self.lock.acquire()
        ret = strid in self.idset
        self.idset.add(strid)
        self.lock.release()
        return ret
   
    def add(self, id):
        strid = str(id)
        self.lock.acquire()
        self.idset.add(strid)
        self.lock.release()
        
class IDMap(object):
    def __init__(self, filename = "idmap.txt"):
        self.lock = threading.Lock()
        self.idmap = {}
        self.filename = filename

    def size(self): 
        return len(self.idmap.keys())

    def loads(self, filename = None):
        if not filename:
            filename = self.filename
        fp = open(filename, "r")
        for line in fp:
            line = line.strip()
            if len(line) <= 2:
                continue
            if line[0] == "#":
                continue
            lst = line.split()
            id = lst[0].strip()
            data = " ".join(lst[1:])
            self.idmap[id] = data
        fp.close()
        
    def dumps(self, filename = None):
        if not filename:
            filename = self.filename
        fp = open(filename, "w")
        for key, val in self.idmap.iteritems():
            fp.write("%s %s\n"%(key, val))
        fp.close()
        
    def check(self, id):
        strid = str(id)
        self.lock.acquire()
        ret = self.idmap.get(strid, None)
        self.lock.release()
        return ret
        
    def check_and_add(self, id, data):
        strid = str(id)
        self.lock.acquire()
        ret = self.idmap.get(strid, None)
        if not ret:
            self.idmap[strid] = data
        self.lock.release()
        return ret
   
    def add(self, id, data):
        strid = str(id)
        self.lock.acquire()
        self.idmap[strid] = data
        self.lock.release()
        
        
if __name__ == "__main__":
    ids = IDSet()
    ids.add("123")
    print ids.check("123"), ids.size()
    print ids.check_and_add("234")
    print ids.check("234"), ids.size()
    print ids.check("234"), ids.size()
    ids.dumps("./tmp.txt")
    ids.loads("./tmp.txt")
    print ids.check("123"), ids.size()
    print ids.check("234"), ids.size()
