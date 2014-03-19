from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

class NusSpider(Spider):
    name = "nus"
    allowed_domains = ["ivle7.nus.edu.sg", "127.0.0.1"]

    # don't forget to serve the page locally with python -m SimpleHTTPServer
    start_urls = [
            "http://127.0.0.1:8000/NUS%20Bulletin.html",
    ]
    base_module_url = "http://ivle7.nus.edu.sg/lms/Account/NUSBulletin/msearch_view_full.aspx?modeCode="

    def parse(self, response):
        """Parse the main module list"""
        sel = Selector(response)
        trs = sel.xpath('//table[@id="result_tbl"]//tr')
        for current_row in trs[2:]:
            module_code = current_row.xpath('.//a[1]/text()').extract()[0]
            yield Request(self.base_module_url+module_code, self.parse_popup)


    def parse_popup(self, response):
        """Parse each popup content individually"""
        sel = Selector(response)
        title = sel.xpath('//table[@id="viewtbl"]/tr[.//*[text()="Module Title"]]')
        print title.xpath('.//td[2]//text()').extract()

