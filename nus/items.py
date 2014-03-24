from scrapy.item import Item, Field

class ProgrammePage(Item):
    url = Field()
    title = Field()

class Module(Item):
    code = Field()
    title = Field()
    description = Field()
    prerequisites = Field()
    credit = Field()
    semester = Field()
    year = Field()
