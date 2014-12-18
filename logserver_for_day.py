#!/usr/bin/python2.6
#-*- coding: utf-8 -*-

'''
Created on 2014-12-18

@author: yao
'''
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from db import Db
import os
import re
import time
import json

client = "logclient20141217.py"

class LogBak():
    def __init__(self):
        self.sndb = Db()
    def main(self,ip,path,regular,isdel,lbtid):
        #验证是否有client脚本
        cmd = """ ssh root@%s "cd /opt;ls -l |grep -w '%s'|wc -l" """ % (ip,client)
        ret = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(ret) == 1:
            pass
        else:
            cmd = """ scp %s root@%s:/opt/ """ % (client,ip)
            os.popen(cmd)
            cmd = """ ssh root@%s "cd /opt;chmod +x %s" """ % (ip,client)
            os.popen(cmd)
        #获取软件类型和系统名称
        cmd = """ curl -s http://itsm.cnsuning.com/traffic-web-in/XOpenApi/ipToSoftStaff.htm?ip=%s """ % ip
        data = os.popen(cmd).readlines()[0]
        ret = json.loads(data)
        systemname,softtype = ret[0]['systemFename'],ret[0]['softType']
        if systemname != "" and softtype != "":
            logpath = path+"/"+regular
            rq =  time.strftime('%Y-%m-%d',time.localtime(time.time() - 60 * 60 * 24) )
            #拼出备份路径
            backuppath = systemname+"/"+rq+"/"+softtype+"/"+ip+"/"
            #print logpath,backuppath,isdel
            cmd = """ssh root@%s "cd /opt;./%s '%s' %s %s" """ % (ip,client,logpath,backuppath,isdel)
            ret = str(os.popen(cmd).readlines()[0].strip('\r\n'))
            if not re.search('fail',ret) and not re.search('exist',ret) and not re.search('problem',ret):
                sql = "update sn_logbacktask set logbacktask_upddate = now(),logbacktask_status = '成功',logbacktask_des = '%s' where logbacktask_id = '%s' " % (ret,lbtid)
                ret = self.sndb.updateInfo(sql)
                if ret == "U-SUCESS":
                    pass
                else:
                    print "%s 更新失败" % lbtid
            else:
                sql = " update sn_logbacktask set logbacktask_upddate = now(),logbacktask_status = '失败',logbacktask_des = '%s' where logbacktask_id = '%s' " % (ret,lbtid)
                ret = self.sndb.updateInfo(sql)
                if ret == "U-SUCESS":
                    pass
                else:
                    print "%s 更新失败" % lbtid
        else:
            msg = "systemname:%s---softtype:%s" % (systemname,softtype)
            sql = " update sn_logbacktask set logbacktask_upddate = now(),logbacktask_status = '失败',logbacktask_des = '%s' where logbacktask_id = '%s' " % (msg,lbtid)
            ret = self.sndb.updateInfo(sql)
            if ret == "U-SUCESS":
                pass
            else:
                print "%s 更新失败" % lbtid
            
class LogBakThread(threading.Thread):
    def __init__(self,threadingSum,ip,path,regular,isdel,lbtid):
        threading.Thread.__init__(self)
        self.threadingSum = threadingSum
        self.ip = ip
        self.path = path
        self.regular = regular
        self.isdel = isdel
        self.lbtid = lbtid
    def run(self):
        with self.threadingSum:
            inst = LogBak()
            inst.main(self.ip,self.path,self.regular,self.isdel,self.lbtid)


if __name__ == '__main__':
    threadingSum = threading.Semaphore(10)
    conn = Db()
    #初始化
    sql = "insert into sn_logbacktask (logbacktask_logbackid,logbacktask_status)  \
           select logback_id,'未开始' from sn_logback where logback_status = '正常' and logback_rate = 'day'"
    ret = conn.insertInfo(sql)
    if ret == "I-SUCESS":
        #获取任务列表
        sql = "select lb.logback_ip,lb.logback_path,lb.logback_regular,lb.logback_isdel,lbt.logbacktask_id from sn_logback lb,sn_logbacktask lbt  \
               where lb.logback_id = lbt.logbacktask_logbackid and lb.logback_rate = 'day' and lbt.logbacktask_status = '未开始'"
        data = conn.selectInfo(sql)
        if str(data) != "S-ERROR" and str(data) != "N-DATA":
            for d in data:
                ip,path,regular,isdel,lbtid = d[0],d[1],d[2],d[3],d[4]
                t = LogBakThread(threadingSum,ip,path,regular,isdel,lbtid)
                t.start()
            for t in threading.enumerate():
                if t is threading.currentThread():
                    continue
                t.join()
        else:
            print "没有符合备份条件的记录."
    else:
        print "初始化失败."
    conn.close()
