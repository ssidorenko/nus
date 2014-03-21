# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Module(Item):
    code = Field()
    title = Field()
    description = Field()
    prerequisites = Field()
    credit = Field()
    semester = Field()
    year = Field()
