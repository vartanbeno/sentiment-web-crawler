from helpers import PAGES, log10, TOTALS, TOTAL_DOCUMENTS, TF


class TFIDF:

    def __init__(self, index, stats):
        """
        Initialize the tf-idf calculator.
        N is the total number of documents, i.e. total number of pages scraped.
        :param index: dictionary of terms, the pages in which they appear, and the number of times they appear in them.
        :param stats: dictionary of pages scraped, with total number of terms, and Afinn score, for each page.
        """
        self.index = index
        self.stats = stats

        self.N = self.stats[TOTALS][TOTAL_DOCUMENTS]

    def get_documents_of_term(self, term):
        """
        From the pages scraped, get those that contain the term in question.
        :param term: a word
        :return: list of web pages
        """
        try:
            return list(self.index[term][PAGES].keys())
        except KeyError:
            return []

    def get_document_frequency_of_term(self, term):
        """
        From the pages scraped, count how many of those have the term in question.
        :param term: a word
        :return: number of pages the term appears in
        """
        try:
            return len(self.get_documents_of_term(term))
        except KeyError:
            return 0

    def get_term_frequency_in_document(self, term, url):
        """
        For the URL of the web page, count how many times the term appears in it.
        :param term: a word
        :param url: a web page
        :return: number of times the term appears in the web page
        """
        try:
            return self.index[term][PAGES][url][TF]
        except KeyError:
            return 0

    def get_idf_weight(self, term):
        """
        Get the inverse document frequency weight of a term.
        :param term: a word
        :return: inverse document frequency of term, or idf
        """
        dft = self.get_document_frequency_of_term(term)
        try:
            return log10(self.N / dft)
        except ZeroDivisionError:
            return 0.0

    def compute_tf_idf(self, term, url):
        """
        Get the term frequency-inverse document frequency of a term in a document in relation to the whole corpus.
        :param term: a word
        :param url: a web page
        :return: tf-idf of word in web page
        """
        tf = self.get_term_frequency_in_document(term, url)
        idf = self.get_idf_weight(term)
        return tf * idf

    dft = get_document_frequency_of_term
    tf = get_term_frequency_in_document
    idf = get_idf_weight
    tf_idf = compute_tf_idf
