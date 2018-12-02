from classes.spider import ConcordiaSpider
from classes.index_builder import IndexBuilder
from classes.document_parser import DocumentParser
from classes.query import Query
from classes.tf_idf import TFIDF

import os
import argparse


output_file = ConcordiaSpider.get_process().settings.get("FEED_URI")


def delete_results():
    if os.path.exists(output_file):
        os.remove(output_file)


parser = argparse.ArgumentParser(description="Configure crawler and set max number of pages it should crawl.")

parser.add_argument("-url", "--start-url", type=str, help="page where we start crawling for links", default="https://www.concordia.ca/about.html")
parser.add_argument("-ign", "--ignore-robots", action="store_true", help="ignore websites' robots.txt", default=False)
parser.add_argument("-l", "--limit", type=int, help="max number of pages to crawl", default=10)

args = parser.parse_args()

if __name__ == '__main__':

    """
    First, delete the results.json file if it exists. The crawler will recreate it and populate it with data.
    Run the crawler through the pages, and from the data in the JSON file, create the inverted index.
    From that same JSON, generate some statistics from the scraped data.
    Finally, prompt the user to conduct some queries against the retrieved data.
    """
    
    delete_results()

    spider = ConcordiaSpider()
    spider.crawl(start_url=args.start_url, obey_robots=not args.ignore_robots, limit=args.limit)
    
    builder = IndexBuilder(output_file)
    builder.construct_index()

    document_parser = DocumentParser(output_file)
    document_parser.construct_stats()

    index = builder.get_index()
    stats = document_parser.get_stats()

    tfidf = TFIDF(index, stats)

    query = Query(index, tfidf)
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

    print("Bye!")
