import re
from functools import reduce
from pandas import Series
from numpy import log10, linalg, dot


def log_tf(tf: int):
    """
    Measures the logarithmic weight of a term inside a document.

    :param tf, an integer indicates term frequency
    :return: logarithmic term frequency if tf > 0; otherwise 0.
    """
    if tf > 0:
        return 1 + log10(tf)
    return 0


def idf(N: int, df: int):
    """
    Measure the informativeness of a term inside a document.

    :param N: The size of the collection.
    :param df: document frequency of a term in a collection.
    :return: logarithmic document frequency known as inverse document frequency
    """
    return log10((N / df))


def normalize(vector: Series):
    """
    Normalize a vector to have a unit length equal to one.

    :param vector: Pandas Series
    :return: the normalized vector.
    """
    return vector / linalg.norm(vector)


def dot_product(S1: Series, S2: Series):
    """
    Used to find the cosine similarity between two vectors.

    :param S1: the first vector: pandas series
    :param S2: the second vector: pandas series
    :return: A scalar value of the dot product between S1 and S2
    """
    return dot(S1, S2)


class Preprocessor:
    @staticmethod
    def remove_stopwords(content: list, lang='english'):
        stopwords = {'english': {
                'ourselves', 'hers', 'between', 'yourself', '', 'a', 'but', 'again', 'there', 'about',
                'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some',
                'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off',
                'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until',
                'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were',
                'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above',
                'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before',
                'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves',
                'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now',
                'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
                'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my',
                'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'
            }}

        return [token for token in content if token not in stopwords[lang]]

    @staticmethod
    def tokenize(string: str, pattern='\\W+'):
        return re.split(pattern, string)

    @staticmethod
    def case_fold(content: list):
        return [term.lower() for term in content]

    def preprocess(self, data: str, tokenize: bool = True, case_folded: bool = True, stopwords: bool = False):
        if len(data) == 0:
            return None

        pipeline = [self.tokenize, self.case_fold, self.remove_stopwords]
        mask = [tokenize, case_folded, stopwords]
        filtered_pipeline = [function for function, boolean in zip(pipeline, mask) if boolean]

        return reduce(lambda content, function: function(content), filtered_pipeline, data)
