# encoding: utf-8
import re
import simplejson as json

from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import HtmlResponse
from porn.items import PageItem

import lxml.html.clean as _clean

_clean.defs.safe_attrs = frozenset(['src', 'href', 'target'])
cleaner = _clean.Cleaner(style=True, remove_unknown_tags=False,
    allow_tags=['a', 'img'])
def clean(data):
    return cleaner.clean_html(data)

tokenizer = re.compile(r'\S[/!?#]?[-\w]*(?:["\'=;]|/?>|:/*)?')
def tokenize(data):
    return [m.group() for m in tokenizer.finditer(data)]


class DomainsSpider(BaseSpider):

    name = "domains"

    def start_requests(self):
        with open(settings.get('DOMAIN_LIST', 'domains'), 'r') as fh:
            for line in fh:
                data = json.loads(line.strip())
                yield self.make_requests_from_url(data['url'])


    def parse(self, response):
        if response.status == 200 and isinstance(response, HtmlResponse):
            body = response.body_as_unicode()
            body = clean(body)
            yield PageItem(url=response.url, body=" ".join(tokenize(body)))
