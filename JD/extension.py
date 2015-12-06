from scrapy import signals
from scrapy.exceptions import NotConfigured
import JD.singleton
import JD.sqlite;

class SpiderOpenClose(object):
 
    def __init__(self, item_count):
        self.item_count = item_count
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler): 
        # first check if the extension should be enabled and raise

        # NotConfigured otherwise

        if not crawler.settings.getbool('MYEXT_ENABLED'): 
            raise NotConfigured

        # get the number of items from settings

        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)
        # instantiate the extension object

        ext = cls(item_count)
        # connect the extension object to signals

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        # crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object

        return ext

    def spider_opened(self, spider):
        pass;     

    def spider_closed(self, spider):
        #pass;
        flag = JD.singleton.getflag()
        if flag["type"] == "full":
            JD.sqlite.JDSQLite().UpdateEndFull(flag["id"]);
        else:
            JD.sqlite.JDSQLite().UpdateEndRemain(flag["id"]);



