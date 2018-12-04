import string
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from afinn import Afinn
from math import log10, sqrt


word_tokenize = word_tokenize
stopwords = set(stopwords.words("english"))
ps = PorterStemmer()
afinn = Afinn()
log10 = log10
sqrt = sqrt


def clean_terms(text):
    """
    :param text: string of text (could be one word, a sentence, a whole article, etc.) to be tokenized and casefolded
    :return: list of terms without strings that are just punctuation, and without stopwords
    """
    terms = word_tokenize(text)
    terms = [term.casefold() for term in terms]
    """ includes the Em dash (a long hyphen), another dash, a kind of single/double quotes, and other punctuation """
    return [term for term in terms if not re.fullmatch("[" + string.punctuation + "–—‘’“”…•‹›«»]+", term)]


SENTIMENT = "sentiment"
PAGES = "pages"
URL = "url"
CONTENT = "content"
TOTALS = "totals"
TOTAL_DOCUMENTS = "total_documents"
TOTAL_TOKENS = "total_tokens"
TOTAL_AFINN = "total_afinn"
AVG_TOKENS = "avg_tokens"
AVG_AFINN = "avg_afinn"

TF = "tf"
CFT = "cft"
DFT = "dft"
IDF = "idf"
TF_IDF = "tf-idf"

COSINE_SIMILARITY = "cosine similarity"
AFINN_SCORE = "Afinn score"
