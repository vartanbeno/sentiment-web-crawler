from sentiment_web_crawler.spiders.spider import ConcordiaSpider
from sentiment_web_crawler.index import Index

import os
import argparse


output_file = ConcordiaSpider.get_process().settings.get("FEED_URI")


def delete_results():
    if os.path.exists(output_file):
        os.remove(output_file)


def get_results():
    if os.path.exists(output_file):
        return "{}/{}".format(os.getcwd(), output_file)


parser = argparse.ArgumentParser(description="Configure Reuters parser and set document limit per block.")
parser.add_argument("-l", "--limit", type=int, help="max number of pages to crawl", default=10)
args = parser.parse_args()

if __name__ == '__main__':

    """
    First, delete the results.json file if it exists. The crawler will recreate it and populate it with data.
    Run the crawler through the pages, and from the data in the JSON file, create the inverted index.
    """

    delete_results()
    ConcordiaSpider.run(args.limit)
    Index(output_file).construct_index()
