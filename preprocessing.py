"""
- Remove Stopwords: Current support English Language Only.
- Tokenize: Tokenize Text based on Non-Character, Consider using other patterns based on the use case.
- case_fold: Casing Folding all tokenized text into lower case. (For Simplicity)
"""

import re
from functools import reduce


class Preprocessor:
    @staticmethod
    def remove_stopwords(content, lang='english'):
        stopwords = {'english': {'ourselves', 'hers', 'between', 'yourself', '', 'a', 'but', 'again', 'there', 'about', 'once',
                                 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for',
                                 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is',
                                 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until',
                                 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were',
                                 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above',
                                 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before',
                                 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves',
                                 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now',
                                 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
                                 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my',
                                 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}}

        return [token for token in content if token not in stopwords[lang]]

    @staticmethod
    def tokenize(string, pattern='\\W+'):
        return re.split(pattern, string)

    @staticmethod
    def case_fold(content):
        return [term.lower() for term in content]

    def preprocess(self, data, tokenize=True, case_folded=True, stopwords=False):
        pipeline = [self.tokenize, self.case_fold, self.remove_stopwords]
        mask = [tokenize, case_folded, stopwords]
        filtered_pipeline = [function for function, boolean in zip(pipeline, mask) if boolean]
        return reduce(lambda content, function: function(content), filtered_pipeline, data)