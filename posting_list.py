"""
- Class Posting represents the basic information of a posting such as the document id, term frequency, more descriptive
  attributes can be added easily.

- Class PostingList represents the A doubly linked list of all postings.
  Keep in mind that each posting is inserted in ascending order by document id to help in query processing.
  Such queries uses INTERSECTION, UNION, NOT, Etc..
"""


class Posting:
    def __init__(self, document_id, term_frequency):
        self.document_id = document_id
        self.term_frequency = term_frequency  # how many times a term occur in the document
        self.next = None
        self.previous = None

    def __repr__(self):
        return f"Posting['document_id': '{self.document_id}', 'term_frequency': '{self.term_frequency}']"


class PostingList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __repr__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.document_id))
            current = current.next

        return ' -> '.join(values) if len(values) != 0 else 'Empty'

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

    def get_postings(self):
        postings = []
        current = self.head
        while current:
            postings.append(current.__repr__())
            current = current.next

        return postings
