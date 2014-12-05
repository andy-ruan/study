#!/usr/bin/env python
# -*-: coding: utf-8 -*-

''' database tools.
    author: andreruan@2011
'''

import os
import os.path
import MySQLdb as MSD

############################################################
class SQLUtil(object):
    def __init__(self,tableName):
        self.m_tableName = tableName
    
    def escapeString(self,strSQL):
        strSQL = strSQL.replace('%', '%%')
        return strSQL
    
    def getSelectSQL(self,selectDomain,whereCondition=None,sortDomain=None):
        strSQL = 'select %s from %s ' % (selectDomain,self.m_tableName)
        strSQL = self.escapeString(strSQL)
        if whereCondition is not None:
            strSQL += 'where %s ' % (whereCondition)
        if sortDomain is not None:
            strSQL += '%s' % (sortDomain)
        return strSQL
    
    def getInsertSQL(self,insertDomain=None,values=''):
        strSQL = 'insert into %s ' % (self.m_tableName)
        if insertDomain is not None:
            strSQL += '(%s) ' % (insertDomain)
        strSQL += ' values(%s)' % (values)
        return self.escapeString(strSQL)
    
    def getUpdateSQL(self,setDomain,whereCondition=None):
        strSQL = 'update %s '%(self.m_tableName)
        strSet = ''
        if type(setDomain) == type(dict):
            strSetList = []
            for key,value in setDomain.items():
                strSetList.append('%s=%s' % (key,value))
            strSet = ','.join(strSetList)    
        elif type(setDomain) == type('') or type(setDomain) == type(u''):
            strSet = setDomain
        else:
            raise Exception('Unsupported setDomain format.')
        
        strSQL += 'set %s' % (strSet)
        strSQL = self.escapeString(strSQL)
        if whereCondition is not None:
            strSQL += ' where %s' % (whereCondition)
        return strSQL
        
    def getDeleteSQL(self,whereCondition=None):
        strSQL = 'delete from %s'(self.m_tableName)
        if whereCondition is not None:
            strSQL += ' where %s' % (whereCondition)
        return strSQL

class DBBase(object):
    def __init__(self, db_name, db_user, db_passwd, db_host, db_port = 3306,charset="utf8"):
        self._m_db_host     = db_host
        self._m_db_port     = db_port
        self._m_db_database = db_name
        self._m_db_user     = db_user
        self._m_db_passwd   = db_passwd
        self._m_db_charset  = charset
        self._m_unix_socket = ''
        self.getConnection()
        
    def __del__(self):
        if self._m_oConn is not None:
            self._m_oConn.close()
            self._m_oConn = None
    
    def beginTransaction(self):
        if self._m_oConn is not None:
            self.endTransaction()
        self.getConnection()
  
    def commit(self):
        if self._m_oConn is not None:
            return self._m_oConn.commit()
        
    def roolBack(self):
        if self._m_oConn is not None:
            return self._m_oConn.rollback()
    
    def endTransaction(self):
        self._m_oConn.commit()
        self._m_oConn.close()
        self._m_oConn = None
    
    def testConnection(self):
        if self._m_oConn is None:
            return False
        else:
            try:
                self._m_oConn.ping()
            except MSD.OperationalError:
                return False
            return True
    
    def getConnection(self):
        try:
            self._m_oConn = MSD.connect(host=self._m_db_host,port=self._m_db_port,
                                        db=self._m_db_database,user=self._m_db_user,
                                        passwd=self._m_db_passwd,#unix_socket='',
                                        charset=self._m_db_charset)
        except Exception,e:
            raise Exception('Error:Connet to %s@%s. Detail : %s.' % (self._m_db_user,self._m_db_host,e))
        
    def executeNoneQuerySQL(self,strSQL,listParams=[]):
        if not self.testConnection():
            self.getConnection()
        if not isinstance(strSQL,(type(''),type(u''))):
            strSQL = str(strSQL)
        try:
            oCursor = self._m_oConn.cursor()
            count = oCursor.execute(strSQL,listParams)
            oCursor.close()
            self._m_oConn.commit()
        except Exception,e:
            raise Exception('Error:Execute sql: %s . Detail : %s' % (strSQL,e))
        return count
    
    def executeQuerySQL(self,strSQL,listParams=[]):
        if not self.testConnection():
            self.getConnection()
        if not isinstance(strSQL,(type(''),type(u''))):
            strSQL = str(strSQL)
        try:
            oCursor = self._m_oConn.cursor()
            oCursor.execute(strSQL,listParams)
            result = oCursor.fetchall()
            oCursor.close()
        except Exception,e:
            raise Exception('Error:Execute sql: %s . Detail : %s' % (strSQL,e))
        return result
    
    def executeCountQuerySQL(self,strSQL,listParams=[]):
        if not self.testConnection():
            self.getConnection()
        result = self.executeQuerySQL(strSQL, listParams)
        if len(result)!=0 and len(result[0])!=0:
            return result[0][0]
        else:
            return None
  
########################################################## 