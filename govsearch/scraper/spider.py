import scrapy

from items import GovtDecisionItem


class GovDecisionSpider(scrapy.Spider):
    name = "gov"
    allowed_domains = ["www.pmo.gov.il"]
    start_urls = [
        "http://www.pmo.gov.il/Secretary/GovDecisions/Pages/default.aspx",
    ]
    custom_settings = {
        'HTTPCACHE_ENABLED': True,
    }

    def parse(self, response):
        print response
        for sel in response.xpath("//div[@id='GDSR']/div/a/@href"):
            yield scrapy.Request(sel.extract(), callback=self.parse_decision_content)

        for sel in response.xpath("//a[@class='PMM-resultsPagingNumber']/@href"):
            url = response.urljoin(sel.extract())

            yield scrapy.Request(url)

    def parse_decision_content(self, response):
        title = response.xpath("//h1[@class='mainTitle']/text()").extract()
        subject = response.xpath("//div[@id='ctl00_PlaceHolderMain_GovXParagraph1Panel']/text()").extract()

        yield GovtDecisionItem(title=title, subject=subject)