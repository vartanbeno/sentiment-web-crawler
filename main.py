from sentiment_web_crawler.spiders.spider import ConcordiaSpider

import os
import argparse


def delete_results():
    if os.path.exists("results.json"):
        os.remove("results.json")


parser = argparse.ArgumentParser(description="Configure Reuters parser and set document limit per block.")
parser.add_argument("-l", "--limit", type=int, help="max number of pages crawled", default=10)
args = parser.parse_args()

if __name__ == '__main__':

    delete_results()
    ConcordiaSpider.run(args.limit)
