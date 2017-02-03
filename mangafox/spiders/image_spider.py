import os
import urllib.request
from bs4 import BeautifulSoup
import scrapy
import time

class ImagesSpider(scrapy.Spider):
    name = "mangafox"
    number = 0
    start_urls = [
        'http://mangafox.me/manga/bleach/'
    ]

    def parse(self, response):
        for manga_number in response.css('a.tips::attr(href)').extract():
            image_page = response.urljoin(manga_number)
            self.number = self.number + 1
            yield scrapy.Request(image_page, self.parse_image)
            time.sleep(1)

    def parse_image(self, response):
        image_url = response.css('img#image::attr(src)').extract()[0]
        urllib.request.urlretrieve(image_url, "imagen_test"+str(self.number)+".jpg")
        yield {'imagen': image_url}
