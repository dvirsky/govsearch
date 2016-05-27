import scrapy


class GovDecisionSpider(scrapy.Spider):
    name = "gov"
    allowed_domains = ["www.pmo.gov.il"]
    start_urls = [
        "http://www.pmo.gov.il/Secretary/GovDecisions/Pages/default.aspx",
    ]

    def parse(self, response):
        for sel in response.xpath("//div[@id='GDSR']/div/a/@href" ):
            yield scrapy.Request(sel.extract(), callback=self.parse_decision_content)
             

        for sel in response.xpath("//a[@class='PMM-resultsPagingNumber']/@href"):
            url = response.urljoin(sel.extract())

            yield scrapy.Request(url)

    def parse_decision_content(self, response):


        title = response.xpath("//h1[@class='mainTitle']/text()").extract()
        print title