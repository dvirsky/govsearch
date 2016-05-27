# -*- coding: utf-8 -*-

import scrapy


class ResolutionItem(scrapy.Item):
    url = scrapy.Field()
    date = scrapy.Field()
    resolution_number = scrapy.Field()
    gov = scrapy.Field()
    title = scrapy.Field()
    subject = scrapy.Field()
    body = scrapy.Field()
