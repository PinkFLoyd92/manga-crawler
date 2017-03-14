import sys
import json
import scrapy
from twisted.internet import reactor, defer
from mangafox.spiders.image_spider import MainSpider
from scrapy.crawler import CrawlerProcess


class Crawler:
    def __init__(self):
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': 'result.json'
        })

    def crawl_image_from_chapter(self, manga_link, chapter):
        self.process.crawl(MainSpider, manga_link,
                           chapter)
        self.process.start()
