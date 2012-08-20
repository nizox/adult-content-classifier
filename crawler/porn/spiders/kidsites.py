# encoding: utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from porn.items import SiteItem

class KidSitesSpider(BaseSpider):

    name = "kidsites"
    start_urls = [ "http://www.goodsitesforkids.org/AtoZ.htm" ]

    def parse(self, response):
        if response.status == 200:
            hxs = HtmlXPathSelector(response)
            for link in hxs.select("//a/@href").extract():
                if link.startswith('http://'):
                    yield KidSiteItem(url=link)
