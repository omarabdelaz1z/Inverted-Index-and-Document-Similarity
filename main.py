from glob import glob
from inverted_index import InvertedIndex


def fetch_content(filename):
    with open(filename, encoding='utf-8', mode='r') as file:
        content = file.read()
        file.close()
        return content


if __name__ == '__main__':
    path = "tmp/*.txt"  # can be changed.
    files = glob(path)
    documents = []

    for file in files:
        documents.append(fetch_content(file))

    inverted_index = InvertedIndex()
    inverted_index.build(documents)
    print(inverted_index.find('different system should results are in cost and can only computing elements'))
