import pandas as pd
from tqdm import tqdm
from lastfm import parsing_article
import pickle


def create_dict(texts: list):
    d = dict()
    ind = 0
    for txt in texts:
        txt = txt.split()
        if txt not in d:
            d[txt] = ind
            ind += 1
    return d


def get_text():
    df = pd.read_csv("./data/playlist_2010to2022.csv")
    lst_txt = []
    for artist in tqdm(df.artist_name.unique()[:20]):
        lst_txt.append(parsing_article(artist, False))
    with open('data.pickle', 'wb') as f:
        pickle.dump(lst_txt, f, pickle.HIGHEST_PROTOCOL)
    return lst_txt


with open('data.pickle', 'rb') as f:
    x = pickle.load(f)
    print(x)
