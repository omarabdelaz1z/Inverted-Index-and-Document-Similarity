import glob
import inverted_index as ii


def fetch_content(filename):
    with open(filename, encoding='utf-8', mode='r') as file:
        content = file.read()
        file.close()
        return content


if __name__ == '__main__':
    path = "tmp/*.txt"  # can be changed.
    files = glob.glob(path)
    documents = []

    for file in files:
        documents.append(fetch_content(file))

    inverted_index = ii.InvertedIndex()
    inverted_index.build_index(documents)

    inverted_index.get_term_info('requirements')

