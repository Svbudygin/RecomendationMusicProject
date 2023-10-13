import argparse
from typing import List, Tuple
import pandas as pd

TRACK_ID_CL = 2
TRACK_NAME_CL = 3
TRACK_POP_CL = 4
ARTIST_CL = 7


def get_table_shape(table: List[List[object]]) -> Tuple[int, int]:
    return len(table) if table else 0, len(table[0]) if len(table) else 0


def get_column_stat(table: List[List[object]], index: int, how: str = "min") -> object:
    if not table:
        return None

    if type(table[0][index]) == list:
        return None

    if how == "min" or how == "max":
        import operator

        comp = operator.gt if how == "max" else operator.lt

        current_value = table[0][index]
        for line in table:
            if comp(line[index], current_value):
                current_value = line[index]

        return current_value


def preprocess_file(file_path: str) -> List[List[object]]:
    df = pd.read_csv(file_path)
    #  TODO: don't use pandas

    return df.values.tolist()


def cosine_similarity(vector1: list, vector2: list):
    ln_vector = len(vector2)
    sm_vector1_vector2 = sum((vector1[i] * vector2[i] for i in range(ln_vector)))
    vector1_squared = sum((vector1[i] ** 2 for i in range(ln_vector))) ** (1 / 2)
    vector2_squared = sum((vector2[i] ** 2 for i in range(ln_vector))) ** (1 / 2)
    return sm_vector1_vector2 / (vector2_squared * vector1_squared)


def get_artist_with_most_songs(table):
    artists = dict()

    for row in table:
        artists[row[ARTIST_CL]] = artists.get(row[ARTIST_CL], 0) + 1

    max_pair = ("", 0)
    for i in artists.items():
        if i[1] > max_pair[1]:
            max_pair = i

    print(sorted(artists.items(), key=lambda pair: pair[1], reverse=True)[:5])

    # artists = [row[ARTIST_CL] for row in table]
    # artists.sort()
    #
    # last_artist = artists[0]
    # last_artist_count = 1
    #
    # max_artist = artists[0]
    # max_artist_count = 1
    #
    # for artist in artists:
    #     if artist == last_artist:
    #         last_artist_count += 1
    #     else:
    #         if max_artist_count <= last_artist_count:
    #             max_artist = last_artist
    #             max_artist_count = last_artist_count
    #         last_artist = artist
    #         last_artist_count = 1

    return max_pair


def get_top_artist_count(table, n=5):
    m = dict()
    for i in table:
        m[i[7]] = m.get(i[7], 0) + 1
    return sorted(m.items(), key=lambda x: x[1], reverse=True)[:n]


def get_top_artist_tracks(table, artist: str, n=5):
    songs = list()
    for row in table:
        if row[ARTIST_CL] == artist:
            songs.append((row[TRACK_NAME_CL], row[TRACK_POP_CL]))

    print(artist)
    for i, song in enumerate(sorted(songs, key=lambda x: x[1], reverse=True)[:n]):
        print(f"{i + 1}) {song[0]}: {song[1]}")


def euclidean_distance(vector_1, vector_2):
    result = 0
    for i in range(len(vector_1)):
        result += (vector_1[i] - vector_2[i]) ** 2

    return result ** 0.5


def get_top_songs_by_sound(table, song_id, n=5):
    base_song_idx = 0
    for i, row in enumerate(table):
        if song_id == row[TRACK_ID_CL]:
            base_song = row[-13:]
            base_song_idx = i
            break

    distances = []
    for i, row in enumerate(table):
        if i == base_song_idx:
            continue
        current = row[-13:]
        distance = euclidean_distance(base_song, current)
        distances.append((distance, i))

    distances.sort()

    return [
        (table[i[1]][TRACK_NAME_CL], table[i[1]][ARTIST_CL], i[0])
        for i in distances[:n]
    ]


def hamming_distance(left_str, right_str):
    dist = 0

    if len(left_str) > len(right_str):
        left_str, right_str = right_str, left_str

    left_str += (len(right_str) - len(left_str)) * "й"

    for i in range(len(right_str)):
        if right_str[i] != left_str[i]:
            dist += 1

    return dist


def jaccard_index(left_str, right_str):
    sim = 0
    lset, rset = set(left_str.split()), set(right_str.split())
    print(lset, rset, lset & rset, lset | rset - lset & rset)

    return len(lset & rset) / (len(lset) + len(rset) - len(lset & rset))


def find_similar_song_name(table, query):
    words = query.lower().split()
    hd_list = list()
    jc_list = list()
    for i, row in enumerate(table):
        hd = hamming_distance(query.lower(), row[TRACK_NAME_CL].lower())
        hd_list.append((hd, i))
        jc = jaccard_index(query.lower(), row[TRACK_NAME_CL].lower())
        jc_list.append((jc, i))

        row_split = row[TRACK_NAME_CL].lower().split()

        if all(x in row_split for x in words):
            print(row[TRACK_NAME_CL])

    print("\n\n----HAMMMING----\n\n")
    hd_list.sort()

    for i, x in hd_list[:5]:
        print(table[x][TRACK_NAME_CL])

    print("\n\n----JACCARD----\n\n")
    jc_list.sort(reverse=True)
    for i, x in jc_list[:5]:
        print(table[x][TRACK_NAME_CL])
        # TODO: fix


def test(table):
    # print(get_table_shape(table))
    # print(get_column_stat(table, 12, "max"))
    # print(get_top_artist_count(table))
    # print(get_artist_with_most_songs(table))
    # get_top_artist_tracks(table, "Rihanna", 10)
    # print(*get_top_songs_by_sound(table, "0wwPcA6wtMf6HUMpIRdeP7", 10), sep="\n")
    (find_similar_song_name(table, "in me"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music Recommendation Application")
    parser.add_argument("file_path", type=str, help="Input file path for table")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show more info or steps"
    )
    parser.add_argument("-s", "--shape", action="store_true", help="Get database shape")
    parser.add_argument("-i", "--column_index", type=int, help="Column index for stats")
    parser.add_argument("-a", "--stats", type=str, choices=["min", "max", "std"])
    parser.add_argument("-t", "--top_artists", type=int)

    # running not in console
    args = parser.parse_args(["./data/playlist_2010to2022.csv"])

    # running in console
    # args = parser.parse_args()

    if args.verbose:
        print(args)
        print(f"File path: {args.file_path}")

    db = preprocess_file(args.file_path)

    if args.shape:
        shape = get_table_shape(db)
        print(f"Database shape: {shape[0]} rows, {shape[1]} columns")

    if args.top_artists:
        n = get_top_artist_count(db, args.top_artists)
        for i, p in enumerate(n):
            print(f"{i + 1}) {p[0]}: {p[1]}")

    if args.column_index:
        print(
            f"{args.stats} is {get_column_stat(db, args.column_index, args.stats)} for {args.column_index} column!"
        )

    test(db)
