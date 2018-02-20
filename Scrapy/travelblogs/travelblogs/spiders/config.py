import scrapy
from scrapy import signals
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import Request
keepup_limit = 4
class Config(scrapy.Spider):
    def __init__(self, name=None, **kwargs):
        super(Config, self).__init__(name, **kwargs)
