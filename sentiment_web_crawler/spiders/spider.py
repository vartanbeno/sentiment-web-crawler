from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import string
import re


stopwords = set(stopwords.words("english"))
ps = PorterStemmer()


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
        Rule(LinkExtractor(deny=[".*twitter.*"]), callback="parse_item", follow=True),
    )

    # xpath expression which will be used to get relevant tags' text content in page's body
    # exclude script/style tags, they're of no interest to the user
    tags = "//body//*[" \
           "self::header | " \
           "self::h1 | self::h2 | self::h3 | self::h4 | self::h5 | self::h6 | " \
           "self::p | self::span | " \
           "self::footer" \
           "]//text()[" \
           "not(parent::script | parent::style)" \
           "]"

    def parse_item(self, response):
        """
        This method parses the response object.
        From the response, we get stuff like the page's title and the content of its body.
        It gets written to the results.json file.

        :param response: response containing the web page's information.
        :return: None
        """
        self.logger.info("Currently scraping: {}".format(response.url))

        url = response.url
        content = []

        title = response.xpath("//title//text()").extract_first()
        content.extend(word_tokenize(title))

        for text in response.xpath(self.tags).extract():
            content.extend(word_tokenize(text))

        # also making sure to remove strings that are only punctuation, and words that are just stopwords
        content = [word.casefold() for word in content]
        content = [ps.stem(word) for word in content
                   if not re.fullmatch("[" + string.punctuation + "]+", word) and word not in stopwords]

        yield {
            "url": url,
            "content": content
        }

    # TODO not sure if we should keep this
    """
    Override the default parse_start_url method, in order to parse the start_url's contents as well.
    """
    parse_start_url = parse_item

    @staticmethod
    def get_process():
        return CrawlerProcess({
            "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
            "ROBOTSTXT_OBEY": True,
            "FEED_FORMAT": "json",
            "FEED_URI": "results.json",
            "CONCURRENT_REQUESTS": 1
        })

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

        :param limit: number of pages to be crawled
        :return: None
        """
        process = ConcordiaSpider.get_process()
        process.settings.set("CLOSESPIDER_ITEMCOUNT", limit)

        process.crawl(ConcordiaSpider)
        process.start()
