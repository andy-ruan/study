#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' log and exception base tools.
    author: andreruan@2011
'''
import sys
import re
import logging
import logging.handlers
import traceback
import subprocess
import os
import os.path

logger = None
############################################################ 
sendrtx = "/usr/local/bin/sendrtxproxy"

class ConsoleHandler(logging.StreamHandler):
    ''' 重写 logging.StreamHandler的输出函数, 支持中文输出. 
        具体参见: lib\logging\__init__.py, class StreamHandler(Handler)
    '''
    def emit(self, record):
        try:
            msg = self.format(record)
            #print msg
            fs = "%s\n"
            self.stream.write(fs % msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
            
def get_logger(name, file="data.log", size = 100 << 20, backup = 5, showConsole = False):
    ''' initial a logger object, 5 backup files each no more than 100M.'''
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    handler = logging.handlers.RotatingFileHandler(file,maxBytes=size,backupCount = backup)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(threadName)s:%(filename)s:%(lineno)d] %(message)s')
    handler.setFormatter(formatter) 
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    if showConsole:
    #    console = logging.StreamHandler()
        console = ConsoleHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)
        logger.addHandler(console)
    #print 'InitLogger [%s] use file [%s]'%(name,file)
    return logger
    
def run_shell(strCommand):
    ''' 
    Description:在 shell 中运行命令 strCommand
    @param (str) strCommand, shell 命令
    @return (False, err_msg) | (True, out_msg) 返回错误信息或者命令行输出
    '''
    p = subprocess.Popen(strCommand,shell=True,close_fds=True,\
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    if p.returncode != 0:
        #print('RunShell Error code [%d][%s]' % (p.returncode, stderrdata.strip()))
        return False,stderrdata
    else:
        return True,stdoutdata
        
def send_rtx(recv_list, title, body, sender = "andreruan"):
    recv = ";".join(recv_list)
    command = "%s %s \"%s\" \"%s\" \"%s\" 0"%(sendrtx, sender, recv, title, body)
    return os.system(command)

def send_sms(recv_list, title, body, sender = "andreruan"):
    recv = ";".join(recv_list)
    command = "%s %s \"%s\" \"%s\" \"%s\" 1"%(sendrtx, sender, recv, title, body)
    return run_shell(command)


    
def get_exception_stack():
    ''' 获得异常堆栈信息
    '''        
    e_type, e_value, e_tb = sys.exc_info()
    msgList = traceback.extract_tb(e_tb)
    msg = '';
    for filename, lineno, name, line in msgList:
        #if line != None and not re.search('raise',line):
        if line != None :
            m1 = '[' + os.path.basename(str(filename)) + ':' + str(lineno) + '] ';
            msg += m1.ljust(22) + str(name).ljust(25) + ' -->  ' + str(line) + '\n';

    eStrType = str(e_type);
    m0 = re.match("<(type|class) '([^)]*)'>",str(e_type));
    if m0:
        eStrType = m0.group(2);
                    
    preList = str(e_value).split('\n');
    m = re.match('^[ \t]*([a-zA-Z0-9\.]*(Exception|Error)): ',preList[-1]);
    if not m: 
        preList[-1] = eStrType + ': ' + preList[-1];

    msg += '\n'.join(preList); 

    return msg;
 
