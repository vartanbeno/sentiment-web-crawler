from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

from sentiment_web_crawler.helpers import clean_terms


class ConcordiaSpider(CrawlSpider):
    """
    The spider starts crawling web pages beginning from the about page of Concordia University's website.
    We define a rule which extracts all links from the page, and calls the 'parse_item' method on each request (link).
    The follow attribute is set to True, meaning that links will be followed from each response extracted by this rule.
    This means the crawler will go from one link, to another from that one, to another from that one, etc.
    """
    name = "ir"
    rules = (
        Rule(LinkExtractor(deny=[".*twitter.*", ".*/fr/.*"]), callback="parse_item", follow=True),
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
        content.extend(clean_terms(title))

        for text in response.xpath(self.tags).extract():
            content.extend(clean_terms(text))

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
        """
        Here, we define a CrawlerProcess, which will help us run the spider from a Python script, instead of using the
        'scrapy' command in the command line.
        More info: https://doc.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script

        Some of the code taken from:
        https://stackoverflow.com/questions/23574636/scrapy-from-script-output-in-json

        :return: CrawlerProcess object
        """
        return CrawlerProcess({
            "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
            "ROBOTSTXT_OBEY": True,
            "FEED_FORMAT": "json",
            "FEED_URI": "results.json",
            "CONCURRENT_REQUESTS": 1
        })

    @staticmethod
    def crawl(start_url="https://www.concordia.ca/about.html", obey_robots=True, limit=10):
        """
        First, we define the start URL of the crawler by appending it to its start_urls attribute, which is currently
        just an empty list.

        In the CrawlerProcess, we define a new ROBOTSTXT_OBEY condition, which specifies whether or not we want to
        respect websites' robots.txt file.

        The CLOSESPIDER_ITEMCOUNT condition closes the spider once x number of links have been scraped. This is useful
        for setting an upper bound on the number of links to visit.

        :param start_url: URL the crawler will start scraping links from
        :param obey_robots: whether or not the crawler will obey websites' robots.txt
        :param limit: max number of pages to be crawled
        :return: None
        """
        ConcordiaSpider.start_urls = [start_url]

        process = ConcordiaSpider.get_process()
        process.settings.set("ROBOTSTXT_OBEY", obey_robots)
        process.settings.set("CLOSESPIDER_ITEMCOUNT", limit)

        process.crawl(ConcordiaSpider)
        process.start()
