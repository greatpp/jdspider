# -*- coding: utf-8 -*-

# Scrapy settings for JD project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'JD'

SPIDER_MODULES = ['JD.spiders']
NEWSPIDER_MODULE = 'JD.spiders'

ITEM_PIPELINES = {'JD.pipelines.MongoDBPipeline': 1, 'JD.pipelines.JDImagesPipeline': 10}

LOG_LEVEL = 'ERROR'

IMAGES_STORE = '/root/workspace/JD/src/JD_PIC' 

SEED_PATH = "/root/workspace/JD/src/jdseed.db3"

EXTENSIONS = {'JD.extension.SpiderOpenClose': 1000,}

MYEXT_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'JD (+http://www.yourdomain.com)'
