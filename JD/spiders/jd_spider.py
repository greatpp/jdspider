# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from JD.items import JdItem
import datetime
import re
import requests
import json
import os
from scrapy.utils.project import get_project_settings
import JD.singleton
import JD.sqlite;
from bs4 import BeautifulSoup
import JD.mongodb
from JD.sqlite import JDSQLite

class JdSpider(scrapy.Spider): 
    name = "jd" 
    allowed_domains = ["jd.com"] 
    
    def checkbelongclass(self, url, belongclass): 
        resp = requests.get(url) 
        soup = BeautifulSoup(resp.text)
        div = soup.findAll('div' , { "class" : "selector" });
        div2 = div[0].findAll('div', {"class":"s-title"});
        b = div2[0].findAll("b");
        if b[0].string == belongclass :
            return True;
        else:
            return False;
        
    def __init__(self, category=None, *args, **kwargs):
        # super(STBSpider, self).__init__(*args, **kwargs)
        # self.start_urls = ["http://item.jd.com/1362052.html"]
        flag = JD.sqlite.JDSQLite().SelWhichGo();
        print flag; 
        if flag == None:
            self.start_urls = [];
        else:
            JD.singleton.editflag(flag);
           
            if flag["type"] == "full":
                if self.checkbelongclass(flag["seedurl"], flag["belongclass"]):
                    self.start_urls = [flag["seedurl"]]
                    JD.sqlite.JDSQLite().UpdateStartFull(flag["id"]);
                else:
                    self.start_urls = [];
                    info = "belongclass改变：【".decode("utf8") + flag["belongclass"] + "】".decode("utf8") + "seedurl：".decode("utf8") + flag["seedurl"] 
                    #print info;
                    JDSQLite().Log(info);
                           #变成状态4 阻止反复运行
                    JD.sqlite.JDSQLite().UpdateEndRemain(flag["id"]);
            else :
                ret = JD.mongodb.JDMongodb().GetRemain(flag["belongclass"], flag["datetime"])
                self.start_urls = ret
                JD.sqlite.JDSQLite().UpdateStartRemain(flag["id"]);
                if len(ret) == 0: 
                    JD.sqlite.JDSQLite().UpdateEndRemain(flag["id"]);
             
    def parse(self, response):
        req = []; 
        if "http://item.jd.com" in response.url : 
            r = Request(response.url, callback=self.parse_subthree);
            req.append(r); 
        else :  
            allcount = response.css('span.fp-text i::text').extract()[0];
            # print allcount;
            for num in range(1, int(allcount) + 1) :
                tempurl = response.url.replace("page=1", "page=" + str(num));
                r = Request(tempurl, callback=self.parse_subone) 
                req.append(r); 
        return req 

    def parse_subone(self, response):
        req = []; 
        urls = response.xpath('//ul[contains(@class, "gl-warp clearfix")]//div[contains(@class, "p-name")]//a/@href').extract();
        for url in urls:
            r = Request(url, callback=self.parse_subtwo);
            req.append(r); 
        return req;
    
    def parse_subtwo(self, response): 
        req = [];
        item = self.parse_subthree(response);
        req.append(item);
        banben = response.css('.p-choose-wrap').xpath('.//div[contains(@class, "item")]').xpath('.//a/@href').extract();
        if len(banben) > 0: 
            for url in banben:
                if "http://item.jd.com" in url : 
                    r = Request(url, callback=self.parse_subthree);
                    req.append(r); 
        return req;
        
    def parse_subthree(self, response):
        print "~~~" + response.url + "*****"; 
        item = JdItem();
        item["url"] = response.url;
        title = response.xpath('//div[@id="name"]/h1/text()').extract(); 
        if len(title) > 0:
            item["title"] = title[0];
        else:
            item["title"] = "";
            
        introduction = response.xpath('//div[@id="product-detail-1"]//ul[@class="p-parameter-list"]').extract();
        if introduction:
            item["introduction"] = self.formatintroduction(introduction[0]);
        else:
            item["introduction"] = "";
                
        specific = response.xpath('//div[@id="product-detail-2"]//table[@class="Ptable"]').extract();
        if specific:
            item["specific"] = self.formatspecific(specific[0]);
        else :
            item["specific"] = "";
         
        belongclass = response.xpath('//div[@class="breadcrumb"]//a/text()').extract();
        if len(belongclass) >= 3:
            item["belongclass"] = belongclass[2];
        else:
            item["belongclass"] = "";
        
        item["adddate"] = datetime.datetime.now();
        item["update"] = datetime.datetime.now();

        sku = self.getsku(response.url);
       
        if sku != "" : 
            try: 
                resp = requests.get('http://p.3.cn/prices/mgets?skuIds=J_' + str(sku)) 
                pricejson = json.loads(resp.text)
                item["price"] = pricejson[0]["p"];
            except:
                item["price"] = "";
                     
        item["brand"] = "";
        
        if item["price"] == "-1" :
            item["isoff"] = "1";
        else:
            item["isoff"] = "0";
        
        settings = get_project_settings() 
        my_setting = settings.get("IMAGES_STORE")
        part1 = sku[0:4]
        part2 = sku[4:]
        imgpath = my_setting + "/jd" + part1 + "/" + part2 + '/';
           
        todownimgs = [];
        imgs = response.xpath('//div[@class="spec-items"]//img/@src').extract();
        for img in  imgs :
            filename = img.split('/')[-1];
            if not os.path.isfile(imgpath + filename):
                todownimgs.append(img.replace("/n5/", "/n1/"))        
        item['image_urls'] = todownimgs;
        # print item['image_urls'];
        item['sku'] = sku;    

        return item;

    def getsku(self, url):
        p = re.compile("/(\d+).html")
        m = p.search(url)
        no = "";
        if m != None: 
            no = m.group(1);
        return no;
    
    def formatspecific(self, strhtml):
        soup = BeautifulSoup(strhtml)
        th = soup.findAll('th' , { "class" : "tdTitle" });
        tr = soup.findAll('tr');
        table = soup.find("table");
        child = {}
        parent = {}
        k = 0
        for j in range(len(th)):
            for i in range(k + 1, len(tr)):
                try:
                    k = i;
                    rows = table.findAll('tr')[i]
                    if rows.find('th') != None:
                        break; 
                    elif len(rows.findAll()) == 0:
                        continue;
                    else:
                        td = rows.findAll('td')
                        if len(td) == 2:
                            child[td[0].string.replace('\n', "")] = td[1].string.replace('\n', "")
                except:
                    continue
            parent[soup.findAll('th')[j].string.replace('\n', "")] = child.copy()
            child.clear()
             
        return json.dumps(parent, ensure_ascii=False)
    
    def formatintroduction(self, html_doc):
        soup = BeautifulSoup(html_doc)
        ul = soup.findAll('ul' , { "class" : "p-parameter-list" });
        ret = {};
        if len(ul) != 0:
            li = ul[0].findAll('li');
            for l in li:
                zu = l.get_text().split('：'.decode('utf8'));
                if len(zu) == 2:
                    ret[zu[0]] = zu[1];
                    
        return json.dumps(ret, ensure_ascii=False)
    
