import scrapy


class GovtDecisionItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    subject = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    number = scrapy.Field()
    government = scrapy.Field()
