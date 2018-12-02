from helpers import afinn, sentiment, pages

import json


class IndexBuilder:

    def __init__(self, file_to_parse):
        """
        Initialize the index builder with the file containing the pages and their content.
        :param file_to_parse: file with the crawler's output
        """
        self.file_to_parse = file_to_parse
        self.index_file = "index.txt"
        self.index = {}

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
                        self.index[term][sentiment] = afinn.score(term)
                        self.index[term][pages] = {}
                    if url not in self.index[term][pages]:
                        self.index[term][pages][url] = 1
                    else:
                        self.index[term][pages][url] += 1

        print("\nIndex created. There's a total of {} distinct terms.".format(len(self.index)))
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
                    index_file.write("{} {}".format(term, index[term][sentiment]))
                    for url, frequency in index[term][pages].items():
                        index_file.write(" {} {}".format(url, frequency))
                    index_file.write("\n")
                except UnicodeEncodeError:
                    pass

    def get_index(self):
        """
        Get the inverted index generated with the above methods.
        :return: the inverted index
        """
        return self.index
