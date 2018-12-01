from sentiment_web_crawler.helpers import clean_terms


class Query:

    def __init__(self, index):
        """
        Query constructor.
        :param index: dictionary generated by the crawler
        """
        self.index = index
        self.original_terms = ""
        self.terms = []

        self.results = []

    @staticmethod
    def ask_user():
        """
        Prompt the user for a query.
        :return: None
        """
        query = input("\nType in a search query.\n")
        print()
        return query

    def get_pages(self, terms):
        """
        Split the query into individual terms.
        For each terms, store in a dictionary the documents in which the term appears (postings list).
        :param: the user's query
        :return: list of postings lists found from the terms in the query
        """
        self.original_terms = terms
        self.terms = clean_terms(terms)

        results = {}

        for term in self.terms:
            try:
                results[term] = self.index[term]["pages"]
            except KeyError:
                results[term] = []

        return list(results.values())

    def execute(self, terms):
        """
        Get pages each term appear in, and conduct their intersection (AND).
        :param terms: the user's query
        :return: list of pages containing all of the terms in the query (AND).
        """
        lists_of_pages = self.get_pages(terms)

        try:
            self.results = sorted(set(lists_of_pages[0]).intersection(*[set(pages) for pages in lists_of_pages[1:]]))
        except IndexError:
            self.results = []

        return self.results

    def print_results(self):
        """
        Print out terms in the query, and the postings found.
        :return: None
        """
        if self.results:
            print("{} page(s) found:\n{}\n".format("{:,}".format(len(self.results)), "\n".join(map(str, self.results))))
        else:
            print("Your search didn't return any results.\n")
