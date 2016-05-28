# -*- coding: utf-8 -*-

import scrapy

from scraper.items import ResolutionItem


class ResolutionSpider(scrapy.Spider):
    name = "resolutions"
    allowed_domains = ["www.pmo.gov.il"]
    start_urls = ["http://www.pmo.gov.il/Secretary/GovDecisions/Pages/default.aspx"]

    def should_retry(self, response):
        """Sometimes body uses anti-scraping tricks.

        e.g. body is:
        <html><body><script>document.cookie='yyyyyyy=ea850ff3yyyyyyy_ea850ff3; path=/';window.location.href=window.location.href;</script></body></html>

        Retrying usually yields a correct response.
        """
        if not response.body.startswith('<html><body><script>'):
            return False

        self.logger.debug('anti-scraping trick for url %s', response.url)

        new_request = response.request.copy()
        new_request.dont_filter = True  # don't de-duplicate the url for retrying

        return new_request

    def parse(self, response):
        """Parse pages containing links to government resolutions."""
        # check if response was bad
        new_request = self.should_retry(response)
        # retry if so
        if new_request:
            yield new_request
            return

        # parse specific resolutions found in current page
        for sel in response.xpath("//div[@id='GDSR']/div/a/@href"):
            yield scrapy.Request(sel.extract(), callback=self.parse_resolution)

        # parse next pages
        for sel in response.xpath("//a[@class='PMM-resultsPagingNumber']/@href"):
            url = response.urljoin(sel.extract())
            yield scrapy.Request(url)

    def parse_resolution(self, response):
        """Scrape relevant fields in specific resolution response."""
        # check if response was bad
        new_request = self.should_retry(response)
        # retry if so
        if new_request:
            yield new_request
            return

        try:
            yield ResolutionItem(
                url=response.url,
                date=response.xpath("/html/head/meta[@name='EventDate']/@content").extract(),
                resolution_number=response.xpath("//*[@id='aspnetForm']/@action").extract(),
                gov=response.xpath("/html/head/meta[@name='Subjects']/@content").extract(),
                title=response.xpath("//h1[@class='mainTitle']//text()").extract(),
                subject=response.xpath("//div[@id='ctl00_PlaceHolderMain_GovXParagraph1Panel']//text()[not(ancestor::h3)]").extract(),
                body=response.xpath("//*[@id='ctl00_PlaceHolderMain_GovXParagraph2Panel']//text()[not(ancestor::h3)]").extract(),
            )
        except AttributeError:
            self.logger.error('bad body in response for url %s and body %s',
                              response.url, response.body)
