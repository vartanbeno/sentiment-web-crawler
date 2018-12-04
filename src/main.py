from classes.spider import ConcordiaSpider
from classes.index_builder import IndexBuilder
from classes.document_parser import DocumentParser
from classes.query import Query
from classes.and_query import AndQuery
from classes.or_query import OrQuery

import os
import argparse


output_file = ConcordiaSpider.get_process().settings.get("FEED_URI")

parser = argparse.ArgumentParser(description="Configure crawler's process.")

parser.add_argument("-url", "--start-url", type=str, help="page where we start crawling for links", default="https://www.concordia.ca/about.html")
parser.add_argument("-ign", "--ignore-robots", action="store_true", help="ignore websites' robots.txt", default=False)
parser.add_argument("-m", "--max", type=int, help="maximum number of pages to crawl", default=10)
parser.add_argument("-skip", "--skip-crawl", action="store_true", help="skip crawler, build index and stats from current results.json", default=False)

args = parser.parse_args()


def delete_results():
    if os.path.exists(output_file):
        os.remove(output_file)


def run_spider():

    """
    First, delete the results.json file if it exists. The crawler will recreate it and populate it with data.
    Run the crawler through the pages, and from the data in the JSON file, generate some statistics for each page.
    From that same JSON, as well as the generated stats, create the inverted index.
    Finally, prompt the user to conduct some queries against the index.
    """

    delete_results()

    spider = ConcordiaSpider()
    spider.crawl(start_url=args.start_url, obey_robots=not args.ignore_robots, max=args.max)

    document_parser = DocumentParser(output_file)
    document_parser.construct_stats()

    stats = document_parser.get_stats()

    index_builder = IndexBuilder(output_file, stats)
    index_builder.construct_index()

    index = index_builder.get_index()

    conduct_queries(index, stats)


def build_stats_and_index():

    stats = DocumentParser.build_stats_from_file()
    index = IndexBuilder.build_index_from_file()

    conduct_queries(index, stats)


def conduct_queries(index, stats):

    and_query = AndQuery(index, stats)
    or_query = OrQuery(index, stats)

    while True:
        user_input = input("Would you like to conduct an AND query or an OR query? Hit enter for no. [and/or] ")
        if user_input == "":
            break
        elif user_input.lower() in ["and", "or"]:
            user_query = Query.ask_user()
            if user_input.lower().strip() == "and":
                and_query.execute(user_query)
            elif user_input.lower().strip() == "or":
                or_query.execute(user_query)


if __name__ == '__main__':

    if not args.skip_crawl:

        run_spider()

    else:

        print("Skipping crawl...")

        if not os.path.exists(IndexBuilder.index_file) or not os.path.exists(DocumentParser.stats_file):

            print(
                "Both {} and {} files have to exist to skip crawling. Run the crawler first to get a data set."
                .format(IndexBuilder.index_file, DocumentParser.stats_file)
            )

        else:

            build_stats_and_index()

    print("Bye!")
