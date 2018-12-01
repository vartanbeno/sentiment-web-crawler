from sentiment_web_crawler.spiders.spider import ConcordiaSpider
from sentiment_web_crawler.index import Index
from sentiment_web_crawler.query import Query

import os
import argparse


output_file = ConcordiaSpider.get_process().settings.get("FEED_URI")


def delete_results():
    if os.path.exists(output_file):
        os.remove(output_file)


def get_results():
    if os.path.exists(output_file):
        return os.path.join(os.getcwd(), output_file)


parser = argparse.ArgumentParser(description="Configure crawler and set max number of pages it should crawl.")

parser.add_argument("-url", "--start-url", type=str, help="page where we start crawling for links", default="https://www.concordia.ca/about.html")
parser.add_argument("-ign", "--ignore-robots", action="store_true", help="ignore websites' robots.txt", default=False)
parser.add_argument("-l", "--limit", type=int, help="max number of pages to crawl", default=10)

args = parser.parse_args()

if __name__ == '__main__':

    """
    First, delete the results.json file if it exists. The crawler will recreate it and populate it with data.
    Run the crawler through the pages, and from the data in the JSON file, create the inverted index.
    Then, parse the index.txt file to retrieve the dictionary.
    """
    
    delete_results()

    spider = ConcordiaSpider()
    spider.crawl(start_url=args.start_url, obey_robots=not args.ignore_robots, limit=args.limit)
    
    i = Index(output_file)
    i.construct_index()
    
    index = i.get_inverted_index()

    query = Query(index)
    choices = {"y": True, "n": False}
    while True:
        user_input = input("Would you like to conduct a query? [y/n] ")
        try:
            if choices[user_input.lower()]:
                user_query = query.ask_user()
                query.execute(user_query)
                query.print_results()
            else:
                break
        except KeyError:
            pass
