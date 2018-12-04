from helpers import afinn, PAGES, URL, CONTENT, TOTALS, TOTAL_DOCUMENTS, TOTAL_TOKENS, TOTAL_AFINN, AVG_TOKENS, AVG_AFINN

import json


class DocumentParser:

    # static variables
    stats_file = "url_stats.txt"
    summary = "SUMMARY:"

    def __init__(self, file_to_parse):
        """
        Initialize the document parser with the file containing the pages and their content.
        A document correspond to a web page.
        :param file_to_parse: file with the crawler's output
        """
        self.file_to_parse = file_to_parse
        self.stats = {PAGES: {}, TOTALS: {}}

    def construct_stats(self):
        """
        Parse the JSON file created by crawler.
        For each result, write the URL, the number of terms parsed, and the total Afinn sentiment score of those terms
        to an output file.
        :return: None
        """
        total_num_tokens = 0
        total_num_afinn = 0

        with open(self.file_to_parse) as file_to_parse:
            results = json.load(file_to_parse)

            for result in results:

                doc_terms = len(result[CONTENT])
                doc_afinn = afinn.score(" ".join(result[CONTENT]))

                total_num_tokens += doc_terms
                total_num_afinn += doc_afinn

                self.stats[PAGES][result[URL]] = {
                    TOTAL_TOKENS: len(result[CONTENT]),
                    TOTAL_AFINN: afinn.score(" ".join(result[CONTENT]))
                }

        self.stats[TOTALS][TOTAL_DOCUMENTS] = len(self.stats[PAGES])
        self.stats[TOTALS][TOTAL_TOKENS] = total_num_tokens
        self.stats[TOTALS][AVG_TOKENS] = total_num_tokens / len(self.stats[PAGES])
        self.stats[TOTALS][TOTAL_AFINN] = total_num_afinn
        self.stats[TOTALS][AVG_AFINN] = total_num_afinn / len(self.stats[PAGES])

        self.write_to_file(self.stats)

    def write_to_file(self, stats):
        """
        Write the statistics of each page to a "url_stats.txt" file.
        Also write a total tally of each statistic at the end.
        :param stats: dictionary containing page statistics
        :return: None
        """
        print("Outputting document stats to {} file...".format(self.stats_file))
        total_num_tokens = 0
        total_num_afinn = 0

        with open(self.stats_file, "w", encoding="utf-8") as stats_file:

            for page, page_info in stats[PAGES].items():

                total_num_tokens += page_info[TOTAL_TOKENS]
                total_num_afinn += page_info[TOTAL_AFINN]

                stats_file.write("{} {} {}\n".format(page, page_info[TOTAL_TOKENS], page_info[TOTAL_AFINN]))

            stats_file.write(
                "\n{} {} document(s): {} total tokens, {} average tokens, {} total Afinn score, {} average Afinn score\n"
                .format(self.summary, len(stats[PAGES]), total_num_tokens, round(total_num_tokens / len(stats[PAGES]), 3), total_num_afinn, round(total_num_afinn / len(stats[PAGES]), 3))
            )

        print("Document stats available at {}, showcasing:\n\t"
              "- each scraped page's URL\n\t"
              "- their total number of terms (non-distinct)\n\t"
              "- their total Afinn sentiment score.\n"
              "It also shows combined statistics of all documents.\n"
              .format(self.stats_file))

    def get_stats(self):
        """
        Get the statistics generated with the above methods.
        :return: the stats
        """
        return self.stats

    @staticmethod
    def build_stats_from_file():
        """
        Build the statistics dictionary from the file.
        :return: statistics dictionary of documents
        """

        stats = {PAGES: {}, TOTALS: {}}

        with open(DocumentParser.stats_file) as stats_file:

            for line in stats_file.readlines():

                elements = line.split()

                if not elements:
                    continue

                if elements[0] == DocumentParser.summary:
                    stats[TOTALS][TOTAL_DOCUMENTS] = int(elements[1])
                    stats[TOTALS][TOTAL_TOKENS] = int(elements[3])
                    stats[TOTALS][AVG_TOKENS] = float(elements[6])
                    stats[TOTALS][TOTAL_AFINN] = float(elements[9])
                    stats[TOTALS][AVG_AFINN] = float(elements[13])
                else:
                    stats[PAGES][elements[0]] = {}
                    stats[PAGES][elements[0]][TOTAL_TOKENS] = int(elements[1])
                    stats[PAGES][elements[0]][TOTAL_AFINN] = float(elements[2])

        return stats
