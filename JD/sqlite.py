# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from scrapy.utils.project import get_project_settings
 
class JDSQLite():
   
    def __init__(self):
        settings = get_project_settings() 
        filepath = settings.get("SEED_PATH")
        self.conn = sqlite3.connect(filepath)
        
    def __del__(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
     
    def UpdateStartFull(self, id):
        self.conn.execute("update Seed set LastFullBeginTime=datetime('now', 'localtime'),Status=1 where id=?", (str(id)))
        self.conn.commit()
    
    def UpdateEndFull(self, id):
        self.conn.execute("update Seed set LastFullEndTime=datetime('now', 'localtime'),Status=2 where id=?", (str(id)))
        self.conn.commit()
       
    def UpdateStartRemain(self, id):
        self.conn.execute("update Seed set LastRemainBeginTime=datetime('now', 'localtime'),Status=3 where id=?", (str(id)))
        self.conn.commit()
    
    def UpdateEndRemain(self, id):
        self.conn.execute("update Seed set LastRemainEndTime=datetime('now', 'localtime'),Status=4 where id=?", (str(id)))
        self.conn.commit()
          
    def SelWhichGo(self) :

        cursor = self.conn.cursor()
          # 优先 0
        cursor.execute(" select id,SeedUrl, BelongClass from Seed where status=0 ");
        val = cursor.fetchall()
        if len(val) > 0:
            return {"id":val[0][0], "seedurl":val[0][1], "type":"full", "belongclass":val[0][2]};
        
          # 1 最早跑的優先
        cursor.execute(" select id,SeedUrl, BelongClass from Seed where status=1 order by LastFullBeginTime ");
        val = cursor.fetchall()
        if len(val) > 0:
            return {"id":val[0][0], "seedurl":val[0][1], "type":"full", "belongclass":val[0][2]};
        
          # 3 上次沒跑結束的
        cursor.execute(" select id, BelongClass,LastFullBeginTime from Seed where status=3 order by LastRemainBeginTime ");
        val = cursor.fetchall()
        if len(val) > 0:
            return {"id":val[0][0], "type":"remain", "belongclass":val[0][1], "datetime":val[0][2]};
        
          # 2 二次处理的
        cursor.execute(" select id, BelongClass, LastFullBeginTime from Seed where status=2 order by LastRemainBeginTime ");
        val = cursor.fetchall()
        if len(val) > 0:
            return {"id":val[0][0], "type":"remain", "belongclass":val[0][1], "datetime":val[0][2]};
         
          # 新一輪開始 大於1天再跑
        cursor.execute(" select id, seedurl, BelongClass  from Seed where status=4 and   LastFullBeginTime  < datetime('now','localtime', '0 day')   order by LastFullBeginTime ");
        val = cursor.fetchall()
        if len(val) > 0:
            return {"id":val[0][0], "seedurl":val[0][1], "type":"full", "belongclass":val[0][2]};
          
    def Log(self, info):
        self.conn.execute("insert into Log (LogTime,Info) values (datetime('now', 'localtime'),?)", (info,))
        self.conn.commit();

# JDSQLite().Log("ririiri日")
# print 1; 
# JDSQLite().UpdateStartFull(1)
# print 1;
# JDSQLite().UpdateEndFull(1)
# print 2
# JDSQLite().UpdateStartRemain(2)
# print 3
# JDSQLite().UpdateEndRemain(2)
# print 4;

# cc = JDSQLite().SelWhichGo();
# print cc;
# 
# print "ok";
