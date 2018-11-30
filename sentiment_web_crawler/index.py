from afinn import Afinn
import json


class Index:

    def __init__(self, file_to_parse):
        """
        Initialize the index builder with the file containing the pages and their content.
        :param file_to_parse: file with the crawler's output
        """
        self.file_to_parse = file_to_parse
        self.index_file = "index.txt"

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
        print("Creating index...")
        with open(self.file_to_parse) as file_to_parse:
            index = {}
            pages = json.load(file_to_parse)

            for page in pages:
                url = page["url"]
                terms = page["content"]

                for term in terms:
                    if term not in index:
                        index[term] = {}
                    if url not in index[term]:
                        index[term][url] = 1
                    else:
                        index[term][url] += 1

        print("Index created. There's a total of {} distinct terms.".format(len(index)))
        self.write_to_file(index)

    def write_to_file(self, index):
        """
        Write the terms with the index.txt file, with their Afinn sentiment value, and the URLs in which they appear, as
        well as the frequency at which they appear in every URL.
        :param index: the inverted index, the keys of which (terms) will be iterated through
        :return: None
        """
        print("Writing index to {} file.".format(self.index_file))
        with open(self.index_file, "w", encoding="utf-8") as index_file:
            for term in sorted(index):
                try:
                    index_file.write("{} {}".format(term, self.get_sentiment_value(term)))
                    for url, frequency in index[term].items():
                        index_file.write(" {} {}".format(url, frequency))
                    index_file.write("\n")
                except UnicodeEncodeError:
                    pass

    @staticmethod
    def get_sentiment_value(text):
        """
        If the text is a list of strings, we join it to form a single string.
        :param text: text that we want the sentiment value of
        :return: sentiment value of text
        """
        a = Afinn()
        if type(text) is str:
            return a.score(text)
        elif type(text) is list:
            return a.score(" ".join(text))
        raise TypeError("Must pass in either a string or a list. Can't pass in a {}.".format(type(text)))

    def get_inverted_index(self):
        """
        Get the inverted index generated with the above methods.
        Basically parses the index.txt file and returns a dictionary object.
        :return: the inverted index
        """
        inverted_index = {}

        with open(self.index_file) as file:

            for line in file.readlines():

                elements = line.split()
                inverted_index[elements[0]] = {}
                inverted_index[elements[0]]['sentiment'] = elements[1]

                for i in range(2, len(elements), 2):
                    inverted_index[elements[0]][elements[i]] = elements[i+1]

        return inverted_index
