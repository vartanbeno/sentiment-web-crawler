from helpers import clean_terms
from classes.query import Query


class OrQuery(Query):

    def __init__(self, index, stats):
        Query.__init__(self, index, stats)

    def execute(self, terms):
        """
        Get pages each term appears in, and conduct their union (OR).
        :param terms: the user's query
        :return: list of pages containing at least one of the terms in the query (OR).
        """
        self.original_terms = terms
        self.terms = clean_terms(terms)
        self.results_with_cosine_similarity = {}

        lists_of_pages = self.get_pages()

        try:
            self.results = set(lists_of_pages[0]).union(*[set(urls) for urls in lists_of_pages[1:]])
            self.get_cosine_similarities()
        except IndexError:
            self.results = []

        self.print_results()
