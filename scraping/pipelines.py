# -*- coding: utf-8 -*-
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
import scrapy
from scrapy.conf import settings
from cStringIO import StringIO
import datetime
from scrapy.pipelines.images import ImagesPipeline, ImageException
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MySQLStorePipeline(object):

    def __init__(self):
#        self.conn = MySQLdb.connect(user='root', '1577292', 'priceua', '127.0.0.1', charset="utf8", use_unicode=True)
        self.conn = MySQLdb.connect(user='root', passwd='12345678', db='flask', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

#class TutorialPipeline(object):
#    def process_item(self, item, spider):
#        return item

    def process_item(self, item, spider):
        # print "========>>>>item[name]", item['laptop']
        try:
            a = "INSERT INTO prices (laptop,price,image,sale,DataCreate)  VALUES (%s, %s, %s, %s, %s)"
            b = (item['laptop'].encode('utf-8'), item['price'], item['image_urls'].split('/')[-1], item['sale'],datetime.date.today())
            self.cursor.execute(a,b)
            get_id = self.conn.insert_id()
            for i,j in zip(item['other_price'],item['other_name']):
                a1 = "INSERT INTO data_prices (price_id,price,site)  VALUES (%s,%s,%s)"
                b1 = (get_id,i,j)
                self.cursor.execute(a1,b1)
            self.conn.commit()
                

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])


        return item
    
class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return Request(item['image_urls']) 
        
    # def item_completed(self, results, item, info):
    #     item['images'] = [x for ok, x in results if ok]
    #     return item
    
    # # Override the convert_image method to disable image conversion    
    # def convert_image(self, image, size=None):
    #     buf = StringIO()        
    #     try:
    #         image.save(buf, image.format)
    #     except Exception, ex:
    #         raise ImageException("Cannot process image. Error: %s" % ex)

    #     return image, buf    
        
    def image_key(self, url):
        # image_guid = hashlib.sha1(url).hexdigest()
        urls = url.split('/')[-1]
        return '%s' % (urls)    
