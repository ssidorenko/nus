from urlparse import urlparse, parse_qs

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

from nus.items import Module

class ModuleLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_item_class = Module

class NusSpider(Spider):
    name = "nus"
    allowed_domains = ["ivle7.nus.edu.sg", "127.0.0.1"]

    # don't forget to serve the page locally with python -m SimpleHTTPServer
    start_urls = [
            "http://127.0.0.1:8000/NUS%20Bulletin.html",
    ]
    base_url = "http://ivle7.nus.edu.sg/lms/Account/NUSBulletin/"
    base_module_url = base_url + "msearch_view_full.aspx?modeCode="


    def parse(self, response):
        """Parse the main module list"""
        sel = Selector(response)
        trs = sel.xpath('//table[@id="result_tbl"]//tr')
        for current_row in trs[2:]:
            # Scrape common module view   
            module_code = current_row.xpath('.//a[1]/text()').extract()[0]
            yield Request(self.base_module_url+module_code, self.parse_popup)

            # Scrape semester modules views
            for href in current_row.xpath('./td[.//img][1]/a/@href').extract():
                # trim javascript:popup('  ')
                href = href.split('popup')[1][2:-2]
                yield Request(self.base_url+href, self.parse_popup)



    def parse_popup(self, response):
        """Parse each popup content individually"""
        loader = ModuleLoader(selector=Selector(response).xpath('//table[@id="viewtbl"]'), response=response)

        if "msearch_view_full.aspx" in response.url:
            # if we're looking at the common view of the module, scrape year/semester from the dropdowns 
            loader.add_xpath('year', '//select[@name="ddAY"]/option[@selected="selected"]/@value')
            loader.add_xpath('semester', '//select[@name="ddSemster"]/option[@selected="selected"]/@value')
        else:
            qs = parse_qs(urlparse(response.url).query)
            loader.add_value('year', qs.get('acadYear'))
            loader.add_value('semester', qs.get('semester'))


        table_items = (
                ('code', 'Module Code'),
                ('title', 'Module Title'),
                ('credit', 'Module Credit'),
                ('description', 'Description'),
                ('prerequisites', 'Prerequisites')
        )

        for (name, label) in table_items:
            loader.add_xpath(name, './tr[.//*[text()="{}"]]/td[2]//text()'.format(label))

        return loader.load_item()

