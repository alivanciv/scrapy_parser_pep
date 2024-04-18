import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

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
                re.sub(
                    r'\D', '', response.css('h1.page-title::text')
                    .get()
                    .split(' – ')[0]
                )
            ),
            'name': response.css('h1.page-title::text').get().split(' – ')[1],
            'status': (
                response
                .xpath('//*[contains(., "Status")]/following-sibling::*')
                .css('abbr::text').get()
            )
        }
        yield PepParseItem(data)
