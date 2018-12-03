from helpers import clean_terms
from classes.query import Query


class AndQuery(Query):

    def __init__(self, index, stats):
        Query.__init__(self, index, stats)

    def execute(self, terms):
        """
        Get pages each term appears in, and conduct their intersection (AND).
        :param terms: the user's query
        :return: list of pages containing all of the terms in the query (AND).
        """
        self.original_terms = terms
        self.terms = clean_terms(terms)
        self.results_with_cosine_similarity = {}

        lists_of_pages = self.get_pages()

        try:
            self.results = set(lists_of_pages[0]).intersection(*[set(urls) for urls in lists_of_pages[1:]])
            self.get_cosine_similarities()
        except IndexError:
            self.results = []

        self.print_results()
