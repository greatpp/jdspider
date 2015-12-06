# -*- coding: utf-8 -*-

from pymongo import MongoClient
import datetime
import requests
import re
import json
import os;
from selenium import webdriver
import codecs
from bs4 import BeautifulSoup
import json  

info = "belongclass改变：【" + "改变"
print info;



str="1315501"
print str[0:4]
print str[4:]

html_doc = """ <ul id="parameter2" class="p-parameter-list">
            <li title="创佳(canca)39HWE6300 F1 39英寸LED全高清液晶平板电视机非安卓电视机 带壁挂底座+礼包">商品名称：创佳(canca)39HWE6300 F1 39英寸LED全高清液晶平板电视机非安卓电视机 带壁挂底座+礼包</li>
            <li title="1449862829">商品编号：1449862829</li>
            <li title="创佳官方旗舰店">店铺： <a href="http://canca.jd.com" target="_blank">创佳官方旗舰店</a></li>
            <li title="2015-06-16 10:04:55">上架时间：2015-06-16 10:04:55</li>
            <li title="12.1kg">商品毛重：12.1kg</li>
            <li title="中国大陆">商品产地：中国大陆</li>
            <li title="LED电视（主流）">品类：LED电视（主流）</li>
            <li title="普通电视">功能：普通电视</li>
            <li title="窄边框">电视选购热点：窄边框</li>
            <li title="39-40英寸">尺寸：39-40英寸</li>
            <li title="不支持">3D：不支持</li>
            <li title="全高清（1920*1080）">分辨率：全高清（1920*1080）</li>
            <li title="客厅电视">居室场景：客厅电视</li>
        </ul>""";

soup = BeautifulSoup(html_doc)
ul = soup.findAll('ul' , { "class" : "p-parameter-list" });
ret = {};
if len(ul) != 0:
    li = ul[0].findAll('li');
    for l in li:
        print l.get_text();
        zu = l.get_text().split('：'.decode('utf8'));
        if len(zu) == 2:
            ret[zu[0]] = zu[1];
print json.dumps(ret, ensure_ascii=False)
    
     
    
# tr=soup.findAll('tr');
# table=soup.find("table");


# parent={}
# print json.dumps(parent,ensure_ascii=False)

# client = MongoClient('192.168.126.130', 27017) 
# db = client["admin"]
# collection = db['jd']
# 
# d = datetime.datetime.strptime("2015-6-19 16:40:10", "%Y-%m-%d %H:%M:%S")
# # print d;
# # return;
# ret = collection.find({"update": {"$gt": d}, "belongclass":"平板1电视"});
# print ret.count();
# 
# for post in ret:
#     print post["url"];
# 
# print 100;
    


# self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')
 
# driver = webdriver.PhantomJS(executable_path='/root/下载/phantomjs-2.0.0/bin/phantomjs')  #这要可能需要制定phatomjs可执行文件的位置
# driver.get("http://product.suning.com/125481023.html") # 抓取页面
# txt= driver.page_source # 打印结果
# file = codecs.open('source2.txt', 'w', encoding='utf-8')
# file.write(txt)
# driver.quit() # 用完记得退出

# print os.path.isdir("/root")

# client = MongoClient('192.168.126.132', 27017)
# db = client["admin"]
# collection = db['jd']
#  
# doc = collection.find_one({'url': "http://item.jd.com/1429812.html"})
# 
# doc["price"] = "300";
# 
# collection.update({'url': "http://item.jd.com/1429812.html"}, doc, False);
# 
# print doc


# post = {"author": "Mike",
#         "text": "My first blog post!",
#         "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.utcnow()}
#  
# #posts = db.posts
# post_id = collection.insert_one(post).inserted_id
# collection.fin
# print post_id

# resp = requests.get('http://p.3.cn/prices/mgets?skuIds=J_1130715')
# 
# print resp.text;
# 
# encodedjson = json.loads(resp.text)
# print encodedjson[0]["p"]


# url="http://item.jd.com/1583392033.html#none"
# p=re.compile("/(\d+).html")
# m=p.search(url)
# 
# print m.group(1) 




