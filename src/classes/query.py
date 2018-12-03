from helpers import clean_terms, afinn, pages, sqrt, style, total_afinn, sentiment
from classes.tf_idf import TFIDF

from beautifultable import BeautifulTable

from abc import abstractmethod


class Query:

    def __init__(self, index, stats):
        """
        Query constructor.
        :param index: dictionary generated by the crawler
        :param stats: dictionary of pages scraped, with total number of terms, and Afinn score, for each page
        """
        self.index = index
        self.stats = stats

        self.tf_idf = TFIDF(self.index, self.stats)

        self.original_terms = ""
        self.terms = []

        self.results = []
        self.results_with_cosine_similarity = {}

        self.table = BeautifulTable(max_width=140, default_alignment=BeautifulTable.ALIGN_LEFT)
        self.table.column_headers = ["cosine similarity", "Afinn score", "URL"]
        self.table.numeric_precision = 10

    @staticmethod
    def ask_user():
        """
        Prompt the user for a query.
        :return: None
        """
        query = input("\nType in a search query.\n")
        print()
        return query

    def get_pages(self):
        """
        Split the query into individual terms.
        For each terms, store in a dictionary the documents in which the term appears (postings list).
        :param: the user's query
        :return: list of postings lists found from the terms in the query
        """
        results = {}

        for term in self.terms:
            try:
                results[term] = self.index[term][pages]
            except KeyError:
                results[term] = []

        return list(results.values())

    def get_tf_idf_of_terms_in_query(self):
        """
        Get tf-idf values of terms in the user's query.
        :return: list of tf-idf values
        """
        tf_idf_values = []

        for term in self.terms:

            term_frequency_in_query = self.terms.count(term)
            term_idf = self.tf_idf.idf(term)

            tf_idf_values.append(term_frequency_in_query * term_idf)

        return tf_idf_values

    def get_tf_idf_of_terms_in_index(self, url):
        """
        Get tf-idf values of terms in the index.
        :return: list of tf-idf values
        """
        tf_idf_values = []

        for term in self.terms:

            term_frequency_in_index = self.tf_idf.tf(term, url)
            term_idf = self.tf_idf.idf(term)

            tf_idf_values.append(term_frequency_in_index * term_idf)

        return tf_idf_values

    def get_cosine_similarities(self):
        """
        For each result obtained from the query, get the cosine similarity between the query and the page. The closer it
        is to 0, the more the query and the document are a match.
        :return: list of cosine similarities between user's query and documents
        """
        tf_idf_to_query = self.get_tf_idf_of_terms_in_query()

        for url in self.results:

            tf_idf_to_index = self.get_tf_idf_of_terms_in_index(url)

            dot_product = sum(i * j for i, j in zip(tf_idf_to_query, tf_idf_to_index))

            vector_norm_query = sqrt(sum(i**2 for i in tf_idf_to_query))
            vector_norm_index = sqrt(sum(i**2 for i in tf_idf_to_index))

            try:
                cosine_similarity = dot_product / (vector_norm_query * vector_norm_index)
            except ZeroDivisionError:
                cosine_similarity = 0.0

            self.results_with_cosine_similarity[url] = {}
            self.results_with_cosine_similarity[url]["cos"] = cosine_similarity
            self.results_with_cosine_similarity[url][sentiment] = self.stats[pages][url][total_afinn]

    def generate_results_table(self, rows):
        """
        Generate a results table from the query.
        :param rows: list of results
        :return: None
        """
        self.table.clear()
        for row in rows:
            self.table.append_row(row)

        print(self.table)

    @abstractmethod
    def execute(self, terms):
        """
        Abstract method, to be implemented by subclasses.
        If run by parent class, will print out message pointing out error.
        :param terms: the user's query.
        :return: None
        """
        if self.__class__.__name__ == "Query":
            print("You are conducting a query using the %s class." % self.__class__.__name__)
            print("Make sure to use either AndQuery or OrQuery.\n")
        return

    def print_results(self):
        """
        Print out terms in the query, and the postings found.
        If the score is positive, print it in green.
        If the score is negative, print it in red.
        If the score is 0, don't print it in a specific colour.

        Results are sorted by cosine similarity.
        The top 10 results are resorted again by sentiment:
         - If the query was overall positive, sort the top 10 descending by sentiment score.
         - If the query was overall negative, sort the top 10 ascending by sentiment score.
         - If the query was neither positive nor negative, keep the results sorted solely by cosine similarity.
        :return: None
        """
        score = afinn.score(self.original_terms)
        if score > 0:
            styled_score = style.light_green(score)
        elif score < 0:
            styled_score = style.light_red(score)
        else:
            styled_score = score

        print("{}: {}\nSentiment value: {}".format(self.__class__.__name__, self.original_terms, styled_score))

        if self.results:

            print("{} page(s) found:".format("{:,}".format(len(self.results))))

            rows = []
            for url, cos_and_score in self.results_with_cosine_similarity.items():
                row = [cos_and_score["cos"], cos_and_score[sentiment], url]
                rows.append(row)

            # sort rows by cosine similarity, ascending
            rows.sort(key=lambda row: row[0], reverse=True)

            # sort top 10 results by sentiment, asc/desc depending on query sentiment
            if score > 0:
                rows = sorted(rows[:10], key=lambda row: row[1], reverse=True) + rows[10:]
            elif score < 0:
                rows = sorted(rows[:10], key=lambda row: row[1]) + rows[10:]

            self.generate_results_table(rows)
            print()

        else:
            print("Your search didn't return any results.\n")
