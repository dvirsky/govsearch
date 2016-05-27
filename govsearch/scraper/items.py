# -*- coding: utf-8 -*-

import scrapy


class GovtDecisionItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    subject = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    number = scrapy.Field()
    government = scrapy.Field()
