#!/usr/bin/python2.6
#-*- coding: utf-8 -*-
'''
Created on 2014-12-17

@author: 11113072
'''

import ftplib
import os
import sys

def upload(files,path,isdel):
    try:
        ftp = ftplib.FTP()
        ftp.connect("10.22.23.192",21)
        ftp.login("1", "1")
    except:
        print "ftp can not connect."
        sys.exit()
    filename = os.path.basename(files)
    try:
        ftp.mkd(path)
    except:
        pass
    ftp.cwd(path)
    file_handler = open(files,'rb')
    bufsize = 1024
    try:
        ftp.storbinary("STOR "+filename,file_handler,bufsize)
        file_handler.close()
        print "%s ftp file sucess." % files
        ftp.quit()
        if int(isdel) == 1:
            delete(files)
        else:
            pass
    except:
        print "reicve file %s fail." % files
        ftp.quit()
        #sys.exit()

def compress(logpath,backpath,isdel):
    path = os.path.dirname(logpath)
    filename = os.path.basename(logpath)
    cmd = "ls %s |grep %s|wc -l" % (path,filename)
    num = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(num) != 0:
        cmd = "ls %s|xargs -I {} gzip {}" % logpath
        os.popen(cmd)
        cmd = "ls %s" % logpath
        filelist = os.popen(cmd).readlines()
        for files in filelist:
            filename = files.strip('\r\n')
            upload(filename,backpath,isdel)
    else:
        print "%s not exist." % logpath

def delete(logpath):
        cmd = "rm -fr %s " % logpath
        os.popen(cmd)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        #logpath = sys.argv[1]
        #backpath = sys.argv[2]
        #isdel = sys.argv[3]
        logpath = '/root/logbak/*$(date +%Y-%m-%d-%H -d "-1 hour")*'
        #logpath = '/root/logbak/*_message.log.$(date -d yesterday +%Y%m%d)*'
        backpath = '1/1'
        isdel = 2
        compress(logpath,backpath,isdel)
    else:
        print "argvs has problem."
