from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

from nltk.tokenize import word_tokenize


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

    # xpath expression which will be used to get relevant tags' text content in page's body
    tags = "//body//*[" \
           "self::header | " \
           "self::h1 | self::h2 | self::h3 | self::h4 | self::h5 | self::h6 | " \
           "self::p | self::span | " \
           "self::footer" \
           "]//text()"

    def parse_item(self, response):
        self.logger.info("Currently scraping: {}".format(response.url))

        url = response.url
        content = []

        title = response.xpath("//title//text()").extract_first()
        content.extend(word_tokenize(title))

        for text in response.xpath(self.tags).extract():
            content.extend(word_tokenize(text))

        # also making sure to remove strings that are only punctuation
        content = [word.lower() for word in content if word.isalpha()]

        yield {
            "url": url,
            "content": content
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
