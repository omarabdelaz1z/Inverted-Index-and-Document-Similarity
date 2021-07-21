from glob import glob
from json import dumps
from inverted_index import InvertedIndex


def fetch_content(filename: str):
    with open(filename, encoding='utf-8', mode='r') as file:
        content = file.read()
        file.close()
        return content


def as_json(data: dict, indent=3):
    return dumps(data, indent=indent)


if __name__ == '__main__':
    path = "tmp/*.txt"  # can be changed.
    files = glob(path)
    documents = {}

    for filename in files:
        documents[filename] = fetch_content(filename)

    inverted_index = InvertedIndex()
    inverted_index.build_index(documents)

    resultSet = inverted_index.find('different system should results are in cost and can only computing elements')
    print(as_json(resultSet))

    termInfo = inverted_index.term_info("agile")
    print(as_json(termInfo))
