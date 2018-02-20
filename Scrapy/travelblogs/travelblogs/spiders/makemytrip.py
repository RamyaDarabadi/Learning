#from scrapy.xlib.pydispatch import dispatcher
from config import *
from db import *
from email import get_email
#import MySQLdb
#import pymysql
class MakeMyTrip(Config):
    """Starts name of the Crawler here"""
    name = "MMT"
    start_urls = ['https://www.makemytrip.com/blog/romantic-places']
    def __init__(self, *args, **kwargs):
        # """Connecting to Database"""
        # self.conn = pymysql.connect(
        #     host="localhost", user="root", password='', 
        #     db="TourTraveldb", charset='utf8mb4')
        # self.cur = self.conn.cursor()
        self.crawl_type = kwargs.get('c_type', 'keepup')
        self.conn , self.cur = get_pymysql_connection()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        #mailer = MailSender(mailfrom = "ramyalatha3004@gmail.com",smtphost  = "smtp.gmail.com", smtpport = 587, smtpuser = "ramyalatha3004@gmail.com", smtppass = "R01491a0237")
        #mailer.send(to = ["raja@emmela.com"], subject = "Test mail : Report", body = "Run completed for Makemytrip Crawler ", cc = ["ramya@emmela.com","ramya@atad.xyz"])
        #get_email('MMT') 
        query = 'insert into travelblogs.run_data(type, sid) values (%s, %s)' 
        values = (self.crawl_type, '1')
        self.cur.execute(query, values)
    def parse(self, response):
        counter = ''
        if self.start_urls[0] == response.url:
            counter = 0
        else:
            counter = response.meta.get('counter', 0)+1
        """Nodes starts here"""
        print response.url
        sel = Selector(response)
        nodes = sel.xpath(
            '//div[@class="category_info row"]//div[@class="category_part col-sm-4 col-xs-12"]')
        for node in nodes:
            """Nodes for required"""
            title = "".join(node.xpath(
                './/div[@class="tile_detail_section append_bottom12"]/p[@class="din-ab text_partinfo search_blog_title append_bottom8"]/a/text()').extract())
            image = "".join(node.xpath('.//p[@class="append_bottom15"]/a/img/@data-src').extract())
            link = "".join(node.xpath(
                './/div[@class="tile_detail_section append_bottom12"]/p[@class="din-ab text_partinfo search_blog_title append_bottom8"]/a/@href').extract())
            publ = "".join(node.xpath(
                './/div[@class="tile_detail_section append_bottom12"]/p[@class="din-ab text_sub_partinfo"]/text()').extract())
            publish = publ.replace('\n\n', '')
            descr = "".join(node.xpath(
                './/p[@class="din-regular image_sub_titleone append_bottom16"]/text()').extract())
            qry = 'insert into mmt(title, descr, image, link, publish, created_at, modified_at)values(%s, %s, %s, %s, %s, now(), now()) on duplicate key update title = %s'
            values = (title, descr, image, link, publish, title)
            #print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()
        next_page_link  = ''.join(sel.xpath('//ul[@class="pagination pagination-lg"]//li[@class="active"]/following-sibling::li[1][not(contains(@class, "disabled"))]/a/@href').extract())
        if next_page_link:
            if self.crawl_type == 'keepup' and counter > keepup_limit:
                next_page_link = ''
            #next_page_link = 'https://www.makemytrip.com/blog/' + next_page_link
            if next_page_link:
                yield Request(next_page_link, callback=self.parse, meta={'counter':counter}) 
