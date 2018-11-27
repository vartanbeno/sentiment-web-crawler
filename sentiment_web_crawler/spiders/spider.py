import scrapy


class Spider(scrapy.Spider):

    name = "ir"

    start_urls = [
        "https://www.concordia.ca/about.html"
    ]

    def parse(self, response):
        for a in response.css('a::attr(href)'):
            yield {'a': a.extract()}
