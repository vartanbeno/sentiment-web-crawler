from helpers import afinn

import json


class DocumentParser:

    def __init__(self, file_to_parse):
        """
        Initialize the document parser with the file containing the pages and their content.
        A document correspond to a web page.
        :param file_to_parse: file with the crawler's output
        """
        self.file_to_parse = file_to_parse
        self.stats_file = "url_stats.txt"

    def write_to_file(self):
        """
        Parse the JSON file created by crawler.
        For each result, write the URL, the number of terms parsed, and the total Afinn sentiment score of those terms
        to an output file.
        :return: None
        """
        with open(self.file_to_parse) as file_to_parse:
            print("Outputting document stats to {} file...".format(self.stats_file))

            with open(self.stats_file, "w", encoding="utf-8") as stats_file:
                results = json.load(file_to_parse)

                for result in results:
                    url = result["url"]
                    terms = result["content"]

                    stats_file.write("{} {} {}\n".format(url, len(terms), afinn.score(" ".join(terms))))

            print("Document stats available at {}, showcasing:\n\t"
                  "- each scraped page's URL\n\t"
                  "- their total number of terms (non-distinct)\n\t"
                  "- their total Afinn sentiment score.\n"
                  .format(self.stats_file))
