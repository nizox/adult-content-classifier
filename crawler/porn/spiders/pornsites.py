# encoding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from porn.items import SiteItem

class PornSitesSpider(CrawlSpider):

    name = "pornsites"
    start_urls = [ "http://www.porndirectory.com" ]
    allowed_domains = [ "porndirectory.com" ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=['//table[@class="categories"]']), callback='parse_category'),
    )

    def parse_category(self, response):
        if response.status == 200:
            hxs = HtmlXPathSelector(response)
            for link in hxs.select('//div[@class="title"]/a/@href').extract():
                if link.startswith('http://'):
                    yield SiteItem(url=link)
