from classes.spider import ConcordiaSpider
from classes.index_builder import IndexBuilder
from classes.document_parser import DocumentParser
from classes.query import Query

from helpers import style

import os
import argparse

output_file = ConcordiaSpider.get_process().settings.get("FEED_URI")


def delete_results():
    if os.path.exists(output_file):
        os.remove(output_file)


parser = argparse.ArgumentParser(description="Configure crawler's process.")

parser.add_argument("-url", "--start-url", type=str, help="page where we start crawling for links", default="https://www.concordia.ca/about.html")
parser.add_argument("-ign", "--ignore-robots", action="store_true", help="ignore websites' robots.txt", default=False)
parser.add_argument("-l", "--limit", type=int, help="max number of pages to crawl", default=10)

args = parser.parse_args()

if __name__ == '__main__':

    """
    First, delete the results.json file if it exists. The crawler will recreate it and populate it with data.
    Run the crawler through the pages, and from the data in the JSON file, generate some statistics for each page.
    From that same JSON, as well as the generated stats, create the inverted index.
    Finally, prompt the user to conduct some queries against the index.
    """
    
    delete_results()

    spider = ConcordiaSpider()
    spider.crawl(start_url=args.start_url, obey_robots=not args.ignore_robots, limit=args.limit)

    document_parser = DocumentParser(output_file)
    document_parser.construct_stats()

    stats = document_parser.get_stats()

    index_builder = IndexBuilder(output_file, stats)
    index_builder.construct_index()

    index = index_builder.get_index()

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

    print(style.light_cyan("Bye!"))
