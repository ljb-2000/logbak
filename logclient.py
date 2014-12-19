#!/usr/bin/python2.6
#-*- coding: utf-8 -*-
'''
Created on 2014-12-17
@author: yao
'''

import ftplib
import os
import sys
import re

class Upload():
    def __init__(self):
        pass
    def main(self,files,path,isdel):
        try:
            ftp = ftplib.FTP()
            ftp.connect("192.168.1.1",21)
            ftp.login("logback", "logback")
        except:
            return "ftp connect fail."
            sys.exit()
        filename = os.path.basename(files)
        try:
            for p in path.split('/')
                ftp.mkd(path)
                ftp.cwd(path)
        except Exception,e:
            if str(e) == "550 Create directory operation failed.":
                return "Create directory operation fail."
            else:
                pass
        #try:
            #ftp.cwd(path)
        #except ftplib.error_perm:
            #ftp.quit()
            #return "Change directory operation fail."
        try:
            file_handler = open(files,'rb')
            bufsize = 1024
            ftp.storbinary("STOR "+filename,file_handler,bufsize)
            file_handler.close()
            ftp.quit()
            if int(isdel) == 1:
                delete(files)
            else:
                pass
            return "%s ftp file sucess." % files
        except Exception,e:
            #print e
            return "reicve file %s fail." % files
            ftp.quit()
            #sys.exit()

def compress(logpath,backpath,isdel):
    path = os.path.dirname(logpath)
    filename = re.sub('\*','',os.path.basename(logpath))
    cmd = "ls %s |grep %s|wc -l" % (path,filename)
    num = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(num) != 0:
        cmd = "ls %s|grep -v gz$|xargs -I {} gzip {}" % logpath
        os.popen(cmd)
        cmd = "ls %s*" % logpath
        filelist = os.popen(cmd).readlines()
        s = ""
        for files in filelist:
            filename = files.strip('\r\n')
            up = Upload()
            ret = up.main(filename,backpath,isdel)
            s+=ret
        print s
    else:
        print "%s not exist." % logpath

def delete(logpath):
        cmd = "rm -fr %s " % logpath
        os.popen(cmd)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        logpath = sys.argv[1]
        backpath = sys.argv[2]
        isdel = sys.argv[3]
        compress(logpath,backpath,isdel)
    else:
        print "argvs has problem."
