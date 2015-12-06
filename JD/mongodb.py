# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import datetime
 
class JDMongodb():
   
    def __init__(self):
        self.client = MongoClient('192.168.126.130', 27017) 
        self.db = self.client["admin"]
        self.collection = self.db['jd']
        
    def __del__(self):
        self.client.close()
        
    def GetRemain(self, belongclass, strdatetime):
        print belongclass;
        print strdatetime;
        ret = [];
        d = datetime.datetime.strptime(strdatetime, "%Y-%m-%d %H:%M:%S") 
        search = self.collection.find({"update": {"$lt": d}, "belongclass":belongclass,"isoff" : "0"}); 
        for post in search:
            ret.append(post["url"]);
        return ret;
        
        
