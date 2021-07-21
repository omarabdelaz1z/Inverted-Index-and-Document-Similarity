from collections import Counter
from posting import PostingList
from utils import idf, Preprocessor


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.preprocessor = Preprocessor()
        self.collection_size = 0
        self.documents = None

    def __repr__(self):
        representation = "{\n\t"
        for key, value in self.index.items():
            representation += f"{key}: {value}\n\t"
        representation += "\n}"

        return representation

    def build_index(self, documents: dict):
        self.collection_size = len(documents)
        self.documents = documents

        for i, (document_name, content) in enumerate(documents.items()):  # used i as an id for a document
            preprocessed_content = self.preprocessor.preprocess(content, stopwords=True)
            occurrences = Counter(preprocessed_content)

            for term in preprocessed_content:
                entry = Term(term)
                term_frequency = occurrences[term]

                if entry not in self.index:
                    self.index[term] = entry

                if not (self.index[term].posting_list.exists(document_id=i)):
                    self.index[term].add(document_id=i, term_frequency=term_frequency)

    def term_info(self, term):
        info = {}
        entry = self.index.get(term)
        if entry is None:
            return info

        info['df'] = entry.document_frequency
        info['idf'] = idf(self.collection_size, entry.document_frequency)
        posting_list = entry.posting_list

        if posting_list.length > 0:
            postings = {}
            for key, value in posting_list.postings.items():
                postings[key] = value

            info['postings_list'] = postings
        else:
            info['postings_list'] = {}

        return info

    def find(self, query):
        """
        Find the documents given query.
        :param query: string.
        :return: Documents
        """
        prepared_query = self.prepare_query(query)
        posting_lists = []

        for term in prepared_query:
            entry = self.index.get(term)
            if entry:
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

            return answer.postings

    def prepare_query(self, query: str):
        prepared_query = self.preprocessor.preprocess(query, stopwords=False)

        return prepared_query


class Term:
    def __init__(self, term: str):
        self.term = term
        self.posting_list = PostingList()
        self.document_frequency = 0

    def add(self, document_id: int, term_frequency: int):
        self.posting_list.insert(document_id, term_frequency)
        self.document_frequency = self.posting_list.length

    def __repr__(self):
        return f"({self.term}, {self.document_frequency}, {self.posting_list})"

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, other):
        return self.term == other

    def __ne__(self, other):
        return not (self == other)


def intersect(P1: PostingList, P2: PostingList):
    """
    Find the intersection between two posting lists. (AND Queries)

    :param P1: the first posting list.
    :param P2: the second posting list
    :return answer: a posting list of all common postings between the given postings lists.
    """
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


def union(P1: PostingList, P2: PostingList):
    """
    Find the union between two posting lists. (OR Queries)

    :param P1: the first posting list.
    :param P2: the second posting list
    :return answer: a posting list of all postings between the given postings lists.
    """
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
