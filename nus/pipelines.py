from scrapy.exceptions import DropItem

class NusPipeline(object):
    def process_item(self, item, spider):
        return item
