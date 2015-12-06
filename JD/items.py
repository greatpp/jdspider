# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JdItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field();
    specific = scrapy.Field();
    introduction = scrapy.Field();
    url = scrapy.Field();
    price = scrapy.Field();
    brand = scrapy.Field();
    belongclass = scrapy.Field();
    adddate = scrapy.Field();
    update = scrapy.Field();
    isoff = scrapy.Field();
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    images = scrapy.Field()
    sku = scrapy.Field()


