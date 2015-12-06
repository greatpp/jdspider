# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import json
import codecs
from collections import OrderedDict
import datetime
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from JD.sqlite import JDSQLite

class MongoDBPipeline(object):

    def __init__(self):
        self.client = MongoClient('192.168.126.130', 27017) 
        self.db = self.client["admin"]
        self.collection = self.db['jd']
        # self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')
 
    def process_item(self, item, spider):
        # line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        # self.file.write(line)
      
        doc = self.collection.find_one({'url': item["url"]})

        if doc == None:
            self.collection.insert_one(dict(item));
        else:
                # 日志追踪 belonclass 方便修改配置
            if item["belongclass"] != doc["belongclass"]:
                info=   "belongclass改变：【".decode("utf8") + doc["belongclass"] + "】=》【".decode("utf8")+ item["belongclass"] + "】url：".decode("utf8")+ item["url"] 
                JDSQLite().Log(info);
                 
            item["adddate"] = doc["adddate"];
            item["brand"] = doc["brand"];
            if item["price"] == "-1":
                item["price"] = doc["price"];
                
            if doc.has_key("image_urls"):
                item["image_urls"].extend(doc["image_urls"]);
                     # 去重
                item["image_urls"] = list(set(item["image_urls"]));
 
                # 为空使用原来的
            item["title"] = self.formatvalue(doc["title"], item["title"]);
            item["introduction"] = self.formatvalue(doc["introduction"], item["introduction"]);
            item["specific"] = self.formatvalue(doc["specific"], item["specific"]);
            item["belongclass"] = self.formatvalue(doc["belongclass"], item["belongclass"]);
                
            self.collection.update({'url':  item["url"]}, OrderedDict(item), False);
        return item
    
    def close_spider(self, spider):
        self.client.close()
     
    def formatvalue(self, oldvalue, newvalue):
        if newvalue == '' or newvalue == '{}':
            return oldvalue;
        else:
            return newvalue;

class JDImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):       
        sku = request.meta['sku'];
           # 拆分成2个文件夹
        part1 = sku[0:4]
        part2 = sku[4:]
        image_guid = request.url.split('/')[-1] 
        ret = "jd" + part1 + "/" + part2 + '/%s' % (image_guid)
        return ret;

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta=item)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
