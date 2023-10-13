import pandas as pd
from tqdm import tqdm
from lastfm import parsing_article
import pickle
from app import cosine_similarity
from math import log2


def tf_term_frequency(word: str, text: str):
    text = text.split()
    return text.count(word) / len(text)


def idf_inverse_document_frequency(word: str, lst_txt: list):
    D = len(lst_txt)
    y = sum((1 for txt in lst_txt if word in txt.split()))
    return log2(D / y)


def vectorize_tf_idf():
    lst = get_text()
    d = create_dict(lst)
    matrix = []
    # for ind, txt in enumerate(lst):
    #     vector = [0] * len(d)
    #     for word in txt.split():
    #         if word in d:
    #             vector[d[word]] += 1
    #     matrix.append(vector)
    # return matrix


def create_dict(texts: list):
    d = dict()
    ind = 0
    for txt in texts:
        for word in txt.split():
            if word not in d:
                d[word] = ind
                ind += 1
    return d


def vectorize():
    lst = get_text()
    d = create_dict(lst)
    matrix = []
    for ind, txt in enumerate(lst):
        vector = [0] * len(d)
        for word in txt.split():
            if word in d:
                vector[d[word]] += 1
        matrix.append(vector)
    return matrix


def fetch_text():
    df = pd.read_csv("./data/playlist_2010to2022.csv")
    lst_txt = []
    for artist in tqdm(df.artist_name.unique()[:20]):
        lst_txt.append(parsing_article(artist, False))
    with open('data.pickle', 'wb') as f:
        pickle.dump(lst_txt, f, pickle.HIGHEST_PROTOCOL)


def get_text():
    with open('data.pickle', 'rb') as f:
        return pickle.load(f)


def tf_function():
    pass


if __name__ == "__main__":
    matrix = vectorize()
    print(cosine_similarity(matrix[0], matrix[1]))
    print(cosine_similarity(matrix[0], matrix[2]))
