# -*- coding: utf-8 -*-

import scrapy

from scraper.items import ResolutionItem


class ResolutionSpider(scrapy.Spider):
    name = "resolutions"
    allowed_domains = ["www.pmo.gov.il"]
    start_urls = [
        "http://www.pmo.gov.il/Secretary/GovDecisions/Pages/default.aspx",
    ]

    def parse(self, response):
        """Parse pages containing links to government resolutions."""
        # parse into specific resolution
        for sel in response.xpath("//div[@id='GDSR']/div/a/@href"):
            yield scrapy.Request(sel.extract(), callback=self.parse_resolution)

        # parse into next pages
        # TODO deduplicate same pages
        for sel in response.xpath("//a[@class='PMM-resultsPagingNumber']/@href"):
            url = response.urljoin(sel.extract())
            yield scrapy.Request(url)

    def parse_resolution(self, response):
        yield ResolutionItem(
            url=response.url,
            date=response.xpath("/html/head/meta[@name='EventDate']/@content").extract(),
            resolution_number=response.xpath("//*[@id='aspnetForm']/@action").extract(),
            gov=response.xpath("/html/head/meta[@name='Subjects']/@content").extract(),
            title=response.xpath("//h1[@class='mainTitle']//text()").extract(),
            subject=response.xpath("//div[@id='ctl00_PlaceHolderMain_GovXParagraph1Panel']//text()[not(ancestor::h3)]").extract(),
            body=response.xpath("//*[@id='ctl00_PlaceHolderMain_GovXParagraph2Panel']//text()[not(ancestor::h3)]").extract(),
        )
