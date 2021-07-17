"""
- Class Posting represents the basic information of a posting such as the document id, term frequency, more descriptive
  attributes can be added easily.

- Class PostingList represents the A doubly linked list of all postings.
  Keep in mind that each posting is inserted in ascending order by document id to help in query processing.
  Such queries uses INTERSECTION, UNION, NOT, Etc..
"""
from CommonMeasures import log_tf


class Posting:
    def __init__(self, document_id, term_frequency):
        self.document_id = document_id
        self.term_frequency = term_frequency  # how many times a term occur in the document
        self.next = None
        self.previous = None

    def __repr__(self):
        return str(self.info)

    @property
    def log_tf(self):
        return log_tf(self.term_frequency)

    @property
    def raw_tf(self):
        return self.term_frequency

    @property
    def info(self):
        return {
            'doc_id': self.document_id,
            'raw_tf': self.raw_tf,
            'log_tf': self.log_tf,
        }


class PostingList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __repr__(self):
        return str(self.postings)

    def insert(self, document_id, term_frequency):
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

    def is_exist(self, document_id):
        current = self.head
        while current:
            if current.document_id == document_id:
                return True
            current = current.next
        return False

    @property
    def postings(self):
        postings = []
        current = self.head
        while current:
            postings.append(current)
            current = current.next

        return {posting.document_id: posting.info for posting in postings}