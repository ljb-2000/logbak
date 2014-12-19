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
    def main(self,filelist,path,isdel):
        try:
            ftp = ftplib.FTP()
            ftp.connect("192.168.1.1",21)
            ftp.login("logback", "logback")
        except:
            return "ftp connect fail."
        try:
            for p in path.split('/'):
                try:
                    ftp.mkd(p)
                    ftp.cwd(p)
                except Exception,e:
                    ftp.cwd(p)
        except Exception,e:
            if str(e) == "550 Create directory operation failed.":
                return "Create directory operation fail."
            else:
                pass
        ret = ""
        try:
            for files in filelist:
                f = files.strip('\r\n')
                filename = os.path.basename(f)
                file_handler = open(f,'rb')
                bufsize = 1024
                ftp.storbinary("STOR "+filename,file_handler,bufsize)
                file_handler.close()
                ret+="%s sucess." % f
                if int(isdel) == 1:
                    delete(f)
                else:
                    pass
        except Exception,e:
            ret+="%s fail." % f
        ftp.quit()
        return ret

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
        up = Upload()
        ret = up.main(filelist,backpath,isdel)
        print ret
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
