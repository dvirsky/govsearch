# -*- coding: utf-8 -*-

import scrapy

from items import GovtDecisionItem


class GovDecisionSpider(scrapy.Spider):
    name = "gov"
    allowed_domains = ["www.pmo.gov.il"]
    start_urls = [
        "http://www.pmo.gov.il/Secretary/GovDecisions/Pages/default.aspx",
    ]

    def parse(self, response):
        """Parse pages containing links to decisions."""
        print response.decode('utf-8')

        # parse into specific decision
        for sel in response.xpath("//div[@id='GDSR']/div/a/@href"):
            yield scrapy.Request(sel.extract(), callback=self.parse_decision_content)

        # parse into next pages
        # TODO deduplicate same pages
        for sel in response.xpath("//a[@class='PMM-resultsPagingNumber']/@href"):
            url = response.urljoin(sel.extract())
            yield scrapy.Request(url)

    def parse_decision(self, response):
        title = response.xpath("//h1[@class='mainTitle']/text()").extract()
        subject = response.xpath(
            "//div[@id='ctl00_PlaceHolderMain_GovXParagraph1Panel']/text()").extract()
        body = response.xpath(
            "//*[@id='ctl00_PlaceHolderMain_GovXParagraph2Panel']/p/text()").extract()
        year =
        id = scrapy.Field()
        url = response.url
        date = response.xpath(
            "/html/head/meta[@name='EventData']/@content").extract()
        number = scrapy.Field()
        government = scrapy.Field()

        yield GovtDecisionItem(title=title, subject=subject)
