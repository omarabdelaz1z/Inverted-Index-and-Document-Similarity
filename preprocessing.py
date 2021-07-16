"""
- Remove Stopwords: Current support English Language Only.
- Tokenize: Tokenize Text based on Non-Character, Consider using other patterns based on the use case.
- case_fold: Casing Folding all tokenized text into lower case. (For Simplicity)
"""

import re


class Preprocessor:
    @staticmethod
    def remove_stopwords(content, lang='english'):
        stopwords = {'english': {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once',
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

    def preprocess(self, content):
        tokenized = self.tokenize(content)
        case_folded = self.case_fold(tokenized)
        no_stopwords = self.remove_stopwords(case_folded)
        return no_stopwords
