import scrapy

from pep_parse.items import PepParseItem
from pep_parse.settings import SPIDER_NAME, ALLOWED_DOMAINS, START_URLS


class PepSpider(scrapy.Spider):
    name = SPIDER_NAME
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def parse(self, response):
        all_peps = (
            response
            .xpath('//section[@id="numerical-index"]')
            .css('tbody')
            .css('tr')
            .css('a::attr(href)')
            .getall()
        )
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': int(
                response.css('h1.page-title::text')
                .get()
                .split(' – ')[0][3:]
            ),
            'name': response.css('h1.page-title::text').get().split(' – ')[1],
            'status': (
                response
                .xpath('//*[contains(., "Status")]/following-sibling::*')
                .css('abbr::text').get()
            )
        }
        yield PepParseItem(data)
