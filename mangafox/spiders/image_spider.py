import urllib.request
import scrapy
from scrapy import signals
import utilities


class MainSpider(scrapy.Spider):

    # manga_link: URL(STRING) chapter:(String)
    def __init__(self, manga_link, chapter):
        self.number_of_pages = 0
        self.download_delay = 1
        self.manga_link = manga_link
        self.start_urls = [manga_link]
        self.chapter = chapter
        self.page_number = 0
        self.last_url = ""
        self.current_url = ""
        self.flag = True

    name = "mangafox"

    def parse(self, response):
        chapter_link = ""
        self.page_number = 1
        self.chapter = utilities.addzeros(self.chapter)

        while True:
            chapter_link = ("http://mangafox.me/manga/"
                            + "%s" % self.manga_link.split('/')[4]
                            + "/c"
                            + "%s" % self.chapter
                            + "/"
                            + "%d" % self.page_number
                            + ".html")
            yield scrapy.Request(chapter_link, self.parse_image)
            if(self.page_number
               == self.number_of_pages + 1) and (self.number_of_pages > 0):
                break

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)

    def parse_image(self, response):
        if(self.flag is True):
            select = response.xpath('//select[contains(@class, "m")]')[0]
            print(select)
            options = select.xpath("//option/@value").extract()
            options = map(int, options)
            self.number_of_pages = max(options)
            self.flag = False

        self.page_number = self.page_number + 1
        image_url = response.css('img#image::attr(src)').extract()[0]
        try:
            urllib.request.urlretrieve(image_url, self.manga_link.split('/')[4]
                                       + str(response.url).split('/')[7][:-5]
                                       + ".jpg")
        except IndexError:
            urllib.request.urlretrieve(image_url, self.manga_link.split('/')[4]
                                       + str(response.url).split('/')[6][:-5]
                                       + ".jpg")
        yield {'imagen': image_url}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MainSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider
