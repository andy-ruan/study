#!/usr/bin/python

import hashlib
import struct

g_dic_topdomain = {
    "ac":0,
    "com":0,
    "edu":0,
    "gov":0,
    "mil":0,
    "arpa":0,
    "net":0,
    "org":0,
    "biz":0,
    "info":0,
    "pro":0,
    "name":0,
    "coop":0,
    "aero":0,
    "museum":0,
    "mobi":0,
    "asia":0,
    "tel":0,
    "int":0,
    "tv":0,
    "travel":0,
    "xxx":0,
    "idv":0,
    "ad":0,
    "ae":0,
    "af":0,
    "ag":0,
    "ai":0,
    "al":0,
    "am":0,
    "an":0,
    "ao":0,
    "aq":0,
    "ar":0,
    "as":0,
    "at":0,
    "au":0,
    "aw":0,
    "az":0,
    "ba":0,
    "bb":0,
    "bd":0,
    "be":0,
    "bf":0,
    "bg":0,
    "bh":0,
    "bi":0,
    "bj":0,
    "bm":0,
    "bn":0,
    "bo":0,
    "br":0,
    "bs":0,
    "bt":0,
    "bv":0,
    "bw":0,
    "by":0,
    "bz":0,
    "ca":0,
    "cc":0,
    "cf":0,
    "cg":0,
    "ch":0,
    "ci":0,
    "ck":0,
    "cl":0,
    "cm":0,
    "cn":0,
    "co":0,
    "cq":0,
    "cr":0,
    "cu":0,
    "cv":0,
    "cx":0,
    "cy":0,
    "cz":0,
    "de":0,
    "dj":0,
    "dk":0,
    "dm":0,
    "do":0,
    "dz":0,
    "ec":0,
    "ee":0,
    "eg":0,
    "eh":0,
    "es":0,
    "et":0,
    "ev":0,
    "fi":0,
    "fj":0,
    "fk":0,
    "fm":0,
    "fo":0,
    "fr":0,
    "ga":0,
    "gb":0,
    "gd":0,
    "ge":0,
    "gf":0,
    "gh":0,
    "gi":0,
    "gl":0,
    "gm":0,
    "gn":0,
    "gp":0,
    "gr":0,
    "gt":0,
    "gu":0,
    "gw":0,
    "gy":0,
    "hk":0,
    "hm":0,
    "hn":0,
    "hr":0,
    "ht":0,
    "hu":0,
    "id":0,
    "ie":0,
    "il":0,
    "in":0,
    "io":0,
    "iq":0,
    "ir":0,
    "is":0,
    "it":0,
    "jm":0,
    "jo":0,
    "jp":0,
    "ke":0,
    "kg":0,
    "kh":0,
    "ki":0,
    "km":0,
    "kn":0,
    "kp":0,
    "kr":0,
    "kw":0,
    "ky":0,
    "kz":0,
    "la":0,
    "lb":0,
    "lc":0,
    "li":0,
    "lk":0,
    "lr":0,
    "ls":0,
    "lt":0,
    "lu":0,
    "lv":0,
    "ly":0,
    "ma":0,
    "mc":0,
    "me":0,
    "md":0,
    "mg":0,
    "mh":0,
    "ml":0,
    "mm":0,
    "mn":0,
    "mo":0,
    "mp":0,
    "mq":0,
    "mr":0,
    "ms":0,
    "mt":0,
    "mv":0,
    "mw":0,
    "mx":0,
    "my":0,
    "mz":0,
    "na":0,
    "nc":0,
    "ne":0,
    "nf":0,
    "ng":0,
    "ni":0,
    "nl":0,
    "no":0,
    "np":0,
    "nr":0,
    "nt":0,
    "nu":0,
    "nz":0,
    "om":0,
    "pa":0,
    "pe":0,
    "pf":0,
    "pg":0,
    "ph":0,
    "pk":0,
    "pl":0,
    "pm":0,
    "pn":0,
    "pr":0,
    "pt":0,
    "pw":0,
    "py":0,
    "qa":0,
    "re":0,
    "ro":0,
    "ru":0,
    "rw":0,
    "sa":0,
    "sb":0,
    "sc":0,
    "sd":0,
    "se":0,
    "sg":0,
    "sh":0,
    "si":0,
    "sj":0,
    "sk":0,
    "sl":0,
    "sm":0,
    "sn":0,
    "so":0,
    "sr":0,
    "st":0,
    "su":0,
    "sy":0,
    "sz":0,
    "tc":0,
    "td":0,
    "tf":0,
    "tg":0,
    "th":0,
    "tj":0,
    "tk":0,
    "tl":0,
    "tm":0,
    "tn":0,
    "to":0,
    "tp":0,
    "tr":0,
    "tt":0,
    "tv":0,
    "tw":0,
    "tz":0,
    "ua":0,
    "ug":0,
    "uk":0,
    "us":0,
    "uy":0,
    "va":0,
    "ve":0,
    "vg":0,
    "vn":0,
    "vu":0,
    "wf":0,
    "ws":0,
    "ye":0,
    "yu":0,
    "za":0,
    "zm":0,
    "zr":0,
    "zw":0
}
def get_md5(str_val):
    val = hashlib.md5(str_val).digest()
    return struct.unpack('QQ', val)[0]
    
def get_sub_domain(url):
    str_url = str(url).strip()
    pos = str_url.find("://")
    if pos == -1:
        return None
    str_tmp = str_url[pos + 3:]
    pos = str_tmp.find("/")
    if pos >= 0:
        str_tmp = str_tmp[:pos]
    lst_tmp = str_tmp.split('.')
    if len(lst_tmp) < 2:
        return None
    pos =  lst_tmp[-1].find(':')
    if pos >= 0:
        lst_tmp[-1] = lst_tmp[-1][:pos]
    str_res = ".".join(lst_tmp)
    return str_res
    
def get_domain(url):
    global g_dic_topdomain
    str_subdomain = get_sub_domain(url)
    if str_subdomain is None:
        return None
    lst_tmp = str_subdomain.split('.')
    if len(lst_tmp) < 2:
        return None
    index = len(lst_tmp)
    flag = False
    cnt = 0
    while not flag and cnt <= 2 and index > 0:
        index -= 1
        if lst_tmp[index] in g_dic_topdomain.iterkeys():
            cnt += 1
        else:
            flag = True
    str_res = ".".join(lst_tmp[index:])
    return str_res

def get_domain_id(url):
    domain = get_domain(url)
    if not domain:
        return 0
    return get_md5(domain)
    
def get_sub_domain_id(url):
    domain = get_sub_domain(url)
    if not domain:
        return 0
    return get_md5(domain)


def test():
    str_url1 = 'http://www.cnblogs.com/xuxm2007/archive/2010/08/30/1812550.html'
    #str_url1 = 'http://v.ku6.com:8080/special/show_6587639/JEcdOUUIgGRW99SKXq0Rjg...html'
    #str_url1 = 'http://www.iqiyi.com'
    #str_url1 = 'http://www.tudou.com/album'
    str_subdomain = get_sub_domain(str_url1)
    str_domain = get_domain(str_url1)
    domain_id = get_domain_id(str_url1)
    sub_domain_id = get_sub_domain_id(str_url1)
    print "Url: " + str(str_url1)
    print "Subdom : " + str(str_subdomain)
    print "Subdomid:" + str(sub_domain_id)
    print "Domain : " + str(str_domain)
    print "Domainid:" + str(domain_id)
    

if __name__ == '__main__':
    test()
        
