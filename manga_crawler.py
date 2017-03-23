from mangafox.spiders.image_spider import MainSpider
# from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
# from config_parser import change_to_manga_dir
from twisted.internet import reactor, defer
from scrapy.settings import Settings


class Crawler:
    def __init__(self):
        settings = Settings()
        settings.setdict({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'DOWNLOAD_DELAY': 2,
            'LOG_LEVEL': 'ERROR'
        }, priority='project')
        self.process = CrawlerRunner(settings=settings)

    def crawl_image_from_chapter(self, manga_link, chapter):
        self.process.crawl(MainSpider, manga_link,
                           chapter)
        self.process.start()

    @defer.inlineCallbacks
    def crawl_multiple(self,
                       manga_link,
                       list_chapter_range,
                       path=None):
        for mng in range(list_chapter_range[0], list_chapter_range[1]+1):
            yield self.process.crawl(MainSpider, manga_link,
                                     str(mng), root_path=path)
        reactor.stop()

    def crawl_image_from_chapters(self,
                                  manga_link,
                                  list_chapter_range,
                                  path=None):
        self.crawl_multiple(manga_link, list_chapter_range, path=path)
        # d = self.process.join()
        # d.addBoth(lambda _: reactor.stop())

        reactor.run()
        # self.process.start()
        # name = manga_link.split('/')[4]
        # change_to_manga_dir(path, name, str(mng))
