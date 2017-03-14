import sys
import json
import scrapy
from twisted.internet import reactor, defer
from mangafox.spiders.image_spider import ImagesSpider
from scrapy.crawler import CrawlerProcess

def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json'
    })

    process.crawl(ImagesSpider, manga_name=sys.argv[1], episode=sys.argv[2])
    process.start()


main()
