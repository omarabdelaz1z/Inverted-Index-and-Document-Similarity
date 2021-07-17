"""
The inverted index consists of terms and its entry such as document frequency, posting list of each term.
"""

from preprocessing import Preprocessor
from posting_list import PostingList
from collections import Counter
import re


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.preprocessor = Preprocessor()

    def __repr__(self):
        representation = "{\n\t"
        for key, value in self.index.items():
            representation += f"{key}: {value}\n\t"
        representation += "\n}"

        return representation

    def build(self, documents):
        for i, document in enumerate(documents):  # used i as an id for a document
            preprocessed_content = self.preprocessor.preprocess(document)
            occurrences = Counter(preprocessed_content)

            for term in preprocessed_content:
                entry = Term(term)
                term_frequency = occurrences[term]

                if entry not in self.index:
                    self.index[term] = entry

                if not (self.index[term].posting_list.is_exist(document_id=i)):
                    self.index[term].add(document_id=i, term_frequency=term_frequency)

    def term_info(self, term):
        entry = self.index.get(term)
        if entry is None:
            return "Term Doesn't Exist"

        print(f"- Term: {term}\n"
              f"- Document Frequency: {entry.document_frequency}\n"
              f"- Postings List: {entry.posting_list.__repr__()}")

        postings = entry.posting_list.get_postings()
        for posting in postings:
            print(f"\t{posting}")

    def find(self, query):
        terms = re.split("\\W+", query)
        posting_lists = []

        for term in terms:
            entry = self.index.get(term)
            if not entry:
                continue
            posting_lists.append(self.index.get(term).posting_list)

        if len(posting_lists) == 1:
            return posting_lists.pop()

        else:
            initial = intersect(posting_lists[0], posting_lists[1])
            answer = None
            for i in range(2, len(posting_lists)):
                current = posting_lists[i]
                answer = intersect(initial, current)
                initial = answer

            return answer


class Term:
    def __init__(self, term):
        self.term = term
        self.posting_list = PostingList()
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
        return not (self == other)


# AND Queries
def intersect(P1, P2):
    answer = PostingList()
    current1, current2 = P1.head, P2.head

    while current1 and current2:
        if current1.document_id == current2.document_id:
            answer.insert(current1.document_id, 0)
            current1 = current1.next
            current2 = current2.next

        elif current1.document_id < current2.document_id:
            current1 = current1.next
        else:
            current2 = current2.next

    return answer


# OR Queries
def union(P1, P2):
    answer = PostingList()
    current1, current2 = P1.head, P2.head

    while current1 and current2:
        if current1.document_id == current2.document_id:
            answer.insert(current1.document_id, 0)
            current1 = current1.next
            current2 = current2.next

        elif current1.document_id < current2.document_id:
            answer.insert(current1.document_id, 0)
            current1 = current1.next
        else:
            answer.insert(current2.document_id, 0)
            current2 = current2.next

        if not current1:
            while current2:
                answer.insert(current2.document_id, 0)
                current2 = current2.next

        elif not current2:
            while current1:
                answer.insert(current1.document_id, 0)
                current1 = current1.next

    return answer
