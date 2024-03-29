from helpers import afinn, SENTIMENT, PAGES, TF, CFT, DFT, IDF, TF_IDF
from classes.tf_idf import TFIDF

import json


class IndexBuilder:

    # static variables
    index_file = "index.txt"

    def __init__(self, file_to_parse, stats):
        """
        Initialize the index builder with the file containing the pages and their content.
        Also pass in a list of stats, which will be used, in conjunction with the index, to compute the tf-idf of terms.
        :param file_to_parse: file with the crawler's output
        :param stats: stats of web pages, such as number of total terms, Afinn score, etc.
        """
        self.file_to_parse = file_to_parse
        self.stats = stats
        self.index = {}

        self.tfidf = TFIDF(self.index, self.stats)

    def construct_index(self):
        """
        Parse the JSON file created by crawler.
        For each object in it (each object has an URL and a list of terms as content):
         - iterate through the terms in the content, storing it in the index.
           • if the term isn't in the index, create a new entry with it as the key, and an empty object {} as its value,
             where we will store the URLs where the term appears.
           • if the term is in the index, check if the current URL is in its value. If it isn't, set the frequency to 1
             (so far); if it is, increment it by 1.
        :return: None
        """
        with open(self.file_to_parse) as file_to_parse:
            results = json.load(file_to_parse)

            for result in results:
                url = result["url"]
                terms = result["content"]

                for term in terms:
                    if term not in self.index:
                        self.index[term] = {}
                        self.index[term][CFT] = 0
                        self.index[term][SENTIMENT] = afinn.score(term)
                        self.index[term][PAGES] = {}
                    self.index[term][CFT] += 1
                    if url not in self.index[term][PAGES]:
                        self.index[term][PAGES][url] = {}
                        self.index[term][PAGES][url][TF] = 1
                    else:
                        self.index[term][PAGES][url][TF] += 1

            for term in self.index:
                self.index[term][DFT] = self.tfidf.dft(term)
                self.index[term][IDF] = self.tfidf.idf(term)
                term_urls = list(self.index[term][PAGES])
                for url in term_urls:
                    self.index[term][PAGES][url][TF_IDF] = self.tfidf.tf_idf(term, url)

        print("Index created. There's a total of {} distinct terms.".format(len(self.index)))
        self.write_to_file(self.index)

    def write_to_file(self, index):
        """
        Write the terms with the index.txt file, with their Afinn sentiment value, and the URLs in which they appear, as
        well as the frequency at which they appear in every URL.
        :param index: the inverted index, the keys of which (terms) will be iterated through
        :return: None
        """
        print("Writing index to {} file...\n".format(self.index_file))
        with open(self.index_file, "w", encoding="utf-8") as index_file:
            for term in sorted(index):
                try:
                    index_file.write("{} {} {} {} {}".format(term, index[term][CFT], index[term][DFT], index[term][IDF], index[term][SENTIMENT]))
                    for url, stats in index[term][PAGES].items():
                        index_file.write(" {} {} {}".format(url, stats[TF], stats[TF_IDF]))
                    index_file.write("\n")
                except UnicodeEncodeError:
                    pass

    def get_index(self):
        """
        Get the inverted index generated with the above methods.
        :return: the inverted index
        """
        return self.index

    @staticmethod
    def build_index_from_file():
        """
        Build the inverted index from the file.
        :return: the inverted index
        """

        index = {}

        with open(IndexBuilder.index_file) as index_file:

            for line in index_file.readlines():

                elements = line.split()

                index[elements[0]] = {}
                index[elements[0]][CFT] = int(elements[1])
                index[elements[0]][DFT] = int(elements[2])
                index[elements[0]][IDF] = float(elements[3])
                index[elements[0]][SENTIMENT] = float(elements[4])

                index[elements[0]][PAGES] = {}

                for i in range (5, len(elements), 3):
                    index[elements[0]][PAGES][elements[i]] = {}
                    index[elements[0]][PAGES][elements[i]][TF] = int(elements[i + 1])
                    index[elements[0]][PAGES][elements[i]][TF_IDF] = float(elements[i + 2])

        return index
