#!/usr/bin/python2.6
#-*- coding: utf-8 -*-
'''
Created on 2014-12-17
@author: yao
'''
import MySQLdb
import sys

class Db():
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='192.168.1.1',user='logback',passwd='logback',db='cmdb',charset="utf8")
            self.cursor = self.conn.cursor()
        except Exception, e:
            print e
            sys.exit()
            
    def selectInfo(self,sql):
        try:
            n = self.cursor.execute(sql)
            if n != 0:
                data = self.cursor.fetchall()
            else:
                data = "N-DATA"
        except Exception:
            data = "S-ERROR"
        return data
    
    def insertInfo(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            result = "I-SUCESS"
        except Exception:
            result = "I-FAIL"
        return result

    def updateInfo(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            result = "U-SUCESS"
        except Exception,e:
            print e
            result = "U-FAIL"
        return result
    
    def close(self):
        self.cursor.close()
        self.conn.close()
