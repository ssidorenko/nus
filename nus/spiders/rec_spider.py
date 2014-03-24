from urlparse import urlparse, parse_qs
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

from nus.items import ProgrammePage

class ProgrammePageLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = ProgrammePage

class RecSpider(CrawlSpider):
    name = "rec"
    allowed_domains = ["nus.edu.sg"]
    start_urls = ["http://www.nus.edu.sg/oam/courses/course.html"]

    rules = (Rule (SgmlLinkExtractor(),
        callback="parse_page", follow=True),
    )

    keywords = {
        "programmes": 10,
        "curriculum": 20,
        "undergraduate": 5
    }
    
    threshold = 40

    def parse_page(self, response):
        loader = ProgrammePageLoader(selector=Selector(response))
        
        current_score = 0

        for (k, score) in self.keywords.viewitems():
            current_score += response.body.lower().count(k) * score

        if current_score > self.threshold:
            loader.add_value("url", response.url)
            loader.add_xpath("title", "//title/text()")
            return loader.load_item() 

