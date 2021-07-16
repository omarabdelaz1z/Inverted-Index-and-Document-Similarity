"""
The inverted index consists of terms and its entry such as document frequency, posting list of each term.
"""


import preprocessing as p
import posting_list as pl
from collections import Counter


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.preprocessor = p.Preprocessor()

    def __repr__(self):
        representation = "{\n\t"
        for key, value in self.index.items():
            representation += f"{key}: {value}\n\t"
        representation += "\n}"

        return representation

    def build_index(self, documents):
        for i, document in enumerate(documents):  # used i as an id for a document
            preprocessed_content = self.preprocessor.preprocess(document)
            occurrences = Counter(preprocessed_content)

            for term in preprocessed_content:
                entry = Term(term)
                term_frequency = occurrences[term]

                if entry not in self.index:
                    self.index[term] = entry

                if not(self.index[term].posting_list.is_exist(document_id=i)):
                    self.index[term].add(document_id=i, term_frequency=term_frequency)

    def get_term_info(self, term):
        entry = self.index.get(term)
        if entry is None:
            return "Term Doesn't Exist"

        print(f"- Term: {term}\n"
              f"- Document Frequency: {entry.document_frequency}\n"
              f"- Postings List: {entry.posting_list.__repr__()}")

        postings = entry.posting_list.get_postings()
        for posting in postings:
            print(f"\t{posting}")


class Term:
    def __init__(self, term):
        self.term = term
        self.posting_list = pl.PostingList()
        self.document_frequency = 0

    def add(self, document_id, term_frequency):
        self.posting_list.insert(document_id, term_frequency)
        self.document_frequency = self.posting_list.length

    def __repr__(self):
        return f"({self.term}, {self.document_frequency}, {self.posting_list})"
        # return f"Term['term':'{self.term}', 'document frequency':{self.document_frequency}]"

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, other):
        return self.term == other

    def __ne__(self, other):
        return not(self == other)
