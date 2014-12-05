#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' Common tools.
    author: andreruan@2013
'''
import os
import sys
import datetime
import time
import hashlib
import struct

##########################################################
def get_module(filename, debug = False):
    conf_path = os.path.dirname(os.path.abspath(filename))
    basename = os.path.basename(filename)
    sys.path.insert(0, conf_path)
    try:
        mod = __import__(basename[:-3])
        reload(mod)
    except:
        sys.path[0] = "."
        if debug:
            raise
        mod = None
    sys.path[0] = "."
    return mod
    
def find_min_N(array, N, cmp = None):
    ''' find and return the top N min item.
        ret[0] the min item,
        ret[1] the 2nd-min one,
        ...
        find_min_N([1,2,3,4,5], 3) will return [1,2,3]
    '''
    length = len(array)
    ret,i  = [], 0
    if length < N * N:
        ret.extend(array)
        ret.sort(cmp)
        ret = ret[:N]
    else:
        while i < length:
            ret.extend(array[i:i+N])
            i += N
            ret.sort(cmp)
            ret = ret[:N]
    return ret
    
def find_max_N(array, N, cmp = None):
    ''' find and return the top N max item.
        ret[0] the max item,
        ret[1] the 2nd-max one,
        ...
        
        find_max_N([1,2,3,4,5], 3) will return [5,4,3]
    '''
    length = len(array)
    ret, i = [], 0
    if length < N * N:
        ret.extend(array)
        ret.sort(cmp)
        ret = ret[-N:]
    else:
        while i < length:
            ret.extend(array[i:i+N])
            i += N
            ret.sort(cmp)
            ret = ret[-N:]
    ret.reverse()
    return ret
     
def unicode_ljust(s, num):
    '''  输出 unicode 格式的对齐. 替换系统函数 unicode.ljust
    
        说明: unicode 的 ljust 有问题, 对不齐.
        len(u"中") == 1
        len(u"中".encode("utf-8")) == 3
        len(u"中".encode("gbk")) == 2
    ''' 
    val_c, val_e = unicode_count(s)
    return s + " " * (num - 2 * val_c - val_e)
        
def unicode_rjust(s, num):
    val_c, val_e = unicode_count(s)
    return " " * (num - 2 * val_c - val_e) + s
 
def unicode_count(s):
    ''' 输出 unicode 串的中文、英文字符个数.
    '''
    val_c = len(s.encode("utf-8")) - len(s.encode("gbk"))
    val_e = len(s) - val_c
    return (val_c, val_e)

def list_to_dict(arr):
    ret = {}
    for each in arr:
        key = each["datetime"]
        val = each["value"]
        ret[key] = val
    return ret
       
def load_config(config_path):
    module = get_module("%s/config.py"%(config_path))
    dict_feature = {}
    attrid_list = []
    for mod in module.feature_config:
        for feature in mod["features"]:
            if feature.get("separator", False):
                continue
            dict_feature[feature["id"]] = feature
            attrid_list.append(feature["id"])
            if not feature.has_key("author"):
                feature["author"] = mod["author"]
    for attr in attrid_list:
        mod = get_module("%s/conf_%s.py"%(config_path, attr))
        if not mod:
            continue
        logger.debug("%s: %s"%(attr, str(mod)))
        dict_feature[attr].update(mod.conf) 
    return module, dict_feature
    
def timestamp2datetime(intval):
    return datetime.datetime.fromtimestamp(int(intval))
    
def datetime2timestamp(dt):
    return int(float(str(time.mktime(dt.timetuple()))))

# return the first n lines.
def getQuery(filename, maxlines = None):
    querys = {}
    fp = open(filename)
    for line in fp:
        line = line.strip()
        if "\t" not in line:
            continue
        fds = line.split("\t")
        if maxlines and len(querys) >= maxlines:
            break
        querys[fds[1]] = fds[0]
    fp.close()
    return querys
    
# return n lines from the two-third part of the file.
def getLastQuery(filename, num):
    querys = {}
    num = max(num, 1)
    c = 0
    for c, l in enumerate(open(filename)): pass
    c += 1
    cnt = c - c / 3;
    fp = open(filename)
    for i in range(cnt): fp.next()
    for line in fp:
        fds = line.strip().split("\t")
        if len(querys) >= num:
            break
        querys[fds[1]] = fds[0]
    fp.close()
    return querys
 
# random select n items from list of querys.
def selectQuery(querys, num):
    index = random.sample(xrange(len(querys)), num)
    return [ querys[each] for each in index ]

# write msg info file, append or overwrite.
def write_file(filename, msg, append=False):
    mode = "w"
    if append:
        mode = "a"
    try:
        fp = open(filename, mode)
        fp.write(msg)
        fp.close()
        return True
    except:
        raise
        return False

def get_md5(str_val):
    val = hashlib.md5(str_val.lower()).digest()
    return struct.unpack('QQ', val)[0]
    #return struct.unpack('Q', hashlib.md5(url).digest()[:8])[0]
  
##########################################################
if __name__ == "__main__":
    url='http://www.iqiyi.com/zongyi/20121111/07cdd7e3df9f1db9.html'
    print get_md5(url)
