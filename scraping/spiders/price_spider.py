# -*- coding: utf-8 -*-
from scraping.items import ProductItem
from scrapy.spiders import CrawlSpider, Rule
import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader import ItemLoader
from scrapy.http.request import Request
from scrapy.item import Item
from itertools import izip_longest

class PriceSpider(CrawlSpider):
    name = "price"
    allowed_domains = ["price.ua"]
    start_urls = [
        "http://price.ua/catc839t1/page.html"
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=(".",)), callback='parse', follow=True)        
    ]

    # def get_laptop(self, response, xpath_selector):
    #     name = ''
    #     if (type(response).__name__ == 'Selector') and xpath_selector:
    #         name = response.xpath(xpath_selector).extract()
    #     return name

    def parse(self, response):
        item = ProductItem() 

        product_xpath = "//div[@class='white-wrap clearer-block']"
        for sel in response.xpath(product_xpath):
            name = sel.xpath("//div[@class='info-wrap']/a/text()").extract()
            price = [ ''.join([j for j in i if j.isdigit()]) for i in sel.xpath("//div[@class='price-wrap']/span/text() | //div[@class='price-wrap']/a/text()").extract() if i != " "]
            image = [ s for s in sel.xpath("//div[@class='photo-wrap']//a//span/img/@src | //div[@class='photo-wrap']//a//span/img/@data-original").extract() if s != '/images/preload.gif']
            sale = sel.xpath("//div[@class='photo-wrap']//a[@class='sale-icon present']").extract()
            other_price = [''.join([pr for pr in oz if pr.isdigit()]) for oz in sel.xpath(".//div[@class='info-wrap']/div/div[3]/div[@class='top5-prices']/span/span[@class='price']/text()").extract() if oz != " " ]
            other_name = sel.xpath(".//div[@class='top5-prices']/span/span[@class='store-name']/text()").extract()

        for item['laptop'],item['price'],item['image_urls'],item['sale'],item['other_name'],item['other_price']  in izip_longest(name,price,image,sale,other_name,other_price):
            if item['sale'] != None:
                item['sale'] = '1'
            else:
                item['sale'] = '0'
            if item['price']:
                item['price'] = int(item['price'])
                if item['price'] < 8000 and item['price'] > 4000:
                    yield item
        print "==========228============"
    

        page_end = int(response.xpath('//span[@id="top-paginator-max"]/text()').extract()[0]) 
        category = response.request.url[:26]
        
        count = int(response.xpath('//li[@class="page selected"]/span/text()').extract()[0])
        if count <= page_end:
            next_page_url = category + "/page" + str(count+1) + ".html"
            request = scrapy.Request(url=next_page_url)
            yield request
