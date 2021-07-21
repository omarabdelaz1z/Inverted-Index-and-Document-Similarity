from utils import log_tf


class Posting:
    """
    Provides the basic information of a posting inside a document such as document id, term frequency.

    Other descriptive attributes can be added such as positioning indexes to allow proximity queries.
    The class act is just a node for a linked list class.
    """

    def __init__(self, document_id, term_frequency):
        self.document_id = document_id
        self.term_frequency = term_frequency
        self.next = None
        self.previous = None

    def __repr__(self):
        return str(self.info)

    @property
    def log_tf(self):
        """
        :return: log_tf: Logarithmic Term Frequency
        """
        return log_tf(self.term_frequency)

    @property
    def raw_tf(self):
        """
        :return: term frequency
        """
        return self.term_frequency

    @property
    def info(self):
        """
        :return: Python Dictionary that describe the Posting.
        """
        return {
            'doc_id': self.document_id,
            'raw_tf': self.raw_tf,
            'log_tf': self.log_tf,
        }


class PostingList:
    """
    Represents the Posting List of a term in the index. The structure used is a doubly linked list.

    Keep in mind that each posting is inserted in ascending order by document id to help in query processing.
    Such queries uses INTERSECTION, UNION.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __repr__(self):
        return str(self.postings)

    def insert(self, document_id: int, term_frequency: int):
        """
        Insert a posting inside the postings list.

        :param document_id: Integer
        :param term_frequency: Integer
        """
        posting = Posting(document_id=document_id, term_frequency=term_frequency)

        if self.head is None:
            self.head = posting
            self.tail = posting
            self.head.previous = None

        elif self.head.document_id > posting.document_id:
            self.head.previous = posting
            posting.next = self.head
            self.head = posting

        elif self.tail.document_id < posting.document_id:
            posting.previous = self.tail
            self.tail.next = posting
            self.tail = posting

        else:
            current = self.head.next
            while current.document_id < posting.document_id:
                current = current.next

            current.previous.next = posting
            posting.previous = current.previous
            current.previous = posting
            posting.next = current

        self.length += 1

    def exists(self, document_id: int):
        """
        Check if a posting exists in a posting list given its document id.

        :param document_id: Integer
        :return: True if exists; False otherwise.
        """
        current = self.head
        while current:
            if current.document_id == document_id:
                return True
            current = current.next
        return False

    @property
    def postings(self):
        """
        All postings inside a posting list.

        :return: (key, value) pairs of document id and posting info.
        """
        postings = {}
        current = self.head
        while current:
            postings[current.document_id] = current.info
            current = current.next

        return postings
