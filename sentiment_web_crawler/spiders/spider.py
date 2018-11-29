from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class ConcordiaSpider(CrawlSpider):
    """
    The spider starts crawling web pages beginning from the about page of Concordia University's website.
    We define a rule which extracts all links from the page, and calls the 'parse_item' method on each request (link).
    The follow attribute is set to True, meaning that links will be followed from each response extracted by this rule.
    This means the crawler will go from one link, to another from that one, to another from that one, etc.
    """
    name = "ir"
    start_urls = [
        "https://www.concordia.ca/about.html"
    ]
    rules = (
        Rule(LinkExtractor(), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        self.logger.info("Currently scraping: {}".format(response.url))
        yield {
            "url": response.url
        }

    @staticmethod
    def run(limit):
        """
        Here, we define a CrawlerProcess, which will help us run the spider from a Python script, instead of using the
        'scrapy' command in the command line.
        More info: https://doc.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script

        In the CrawlerProcess, we can define a CLOSESPIDER_ITEMCOUNT condition, which closes the spider once x number of
        links have been scraped. This is useful for setting an upper bound on the number of links to visit.

        The ROBOTSTXT_OBEY set to True prevents us from scraping links that are in a website's robots.txt file.

        Some of the code taken from:
        https://stackoverflow.com/questions/23574636/scrapy-from-script-output-in-json

        :return: None
        """
        process = CrawlerProcess({
            "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
            "ROBOTSTXT_OBEY": True,
            "CLOSESPIDER_ITEMCOUNT": limit,
            "FEED_FORMAT": "json",
            "FEED_URI": "results.json"
        })

        process.crawl(ConcordiaSpider)
        process.start()
