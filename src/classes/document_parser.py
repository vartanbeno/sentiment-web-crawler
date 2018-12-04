from helpers import afinn, pages, url, content, totals, total_documents, total_tokens, total_afinn, avg_tokens, avg_afinn

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
        self.stats = {pages: {}, totals: {}}

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

                doc_terms = len(result[content])
                doc_afinn = afinn.score(" ".join(result[content]))

                total_num_tokens += doc_terms
                total_num_afinn += doc_afinn

                self.stats[pages][result[url]] = {
                    total_tokens: len(result[content]),
                    total_afinn: afinn.score(" ".join(result[content]))
                }

        self.stats[totals][total_documents] = len(self.stats[pages])
        self.stats[totals][total_tokens] = total_num_tokens
        self.stats[totals][avg_tokens] = total_num_tokens / len(self.stats[pages])
        self.stats[totals][total_afinn] = total_num_afinn
        self.stats[totals][avg_afinn] = total_num_afinn / len(self.stats[pages])

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

            for page, page_info in stats[pages].items():

                total_num_tokens += page_info[total_tokens]
                total_num_afinn += page_info[total_afinn]

                stats_file.write("{} {} {}\n".format(page, page_info[total_tokens], page_info[total_afinn]))

            stats_file.write(
                "\n{} {} document(s): {} total tokens, {} average tokens, {} total Afinn score, {} average Afinn score\n"
                .format(self.summary, len(stats[pages]), total_num_tokens, round(total_num_tokens / len(stats[pages]), 3), total_num_afinn, round(total_num_afinn / len(stats[pages]), 3))
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

        stats = {pages: {}, totals: {}}

        with open(DocumentParser.stats_file) as stats_file:

            for line in stats_file.readlines():

                elements = line.split()

                if not elements:
                    continue

                if elements[0] == DocumentParser.summary:
                    stats[totals][total_documents] = int(elements[1])
                    stats[totals][total_tokens] = int(elements[3])
                    stats[totals][avg_tokens] = float(elements[6])
                    stats[totals][total_afinn] = float(elements[9])
                    stats[totals][avg_afinn] = float(elements[13])
                else:
                    stats[pages][elements[0]] = {}
                    stats[pages][elements[0]][total_tokens] = int(elements[1])
                    stats[pages][elements[0]][total_afinn] = float(elements[2])

        return stats
