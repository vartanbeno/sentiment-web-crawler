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
            total_terms = 0
            total_afinn = 0

            with open(self.stats_file, "w", encoding="utf-8") as stats_file:
                results = json.load(file_to_parse)

                for result in results:
                    url = result["url"]
                    terms = result["content"]

                    doc_terms = len(terms)
                    doc_afinn = afinn.score(" ".join(terms))

                    total_terms += doc_terms
                    total_afinn += doc_afinn

                    stats_file.write("{} {} {}\n".format(url, doc_terms, doc_afinn))

                stats_file.write("\n{} documents: {} total tokens, {} total Afinn score, {} average Afinn score\n"
                                 .format(len(results), total_terms, total_afinn, round(total_afinn/len(results), 3)))

            print("Document stats available at {}, showcasing:\n\t"
                  "- each scraped page's URL\n\t"
                  "- their total number of terms (non-distinct)\n\t"
                  "- their total Afinn sentiment score.\n"
                  .format(self.stats_file))
