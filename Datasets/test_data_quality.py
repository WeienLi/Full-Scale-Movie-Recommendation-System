import os

import pandas as pd

self_dir = os.path.dirname(__file__)

# data_movie. Do not care => check data_movie_processed

# Test rest:
# data_movie_processed.csv is used for M2. Checking for NA, binng age 1 to 5, splitting genre 0 or 1,
# watch_rating_1 and watch_rating_2


def test_data_quality():
    assert True


def test_data_movie_processed():
    print("test_movie_processed")

    path_to_file = os.path.join(self_dir, "../Datasets/data_movie_processed.csv")

    movies = pd.read_csv(path_to_file, sep=";")
    column_0 = "movieID;vote_average;popularity;original_language".split(";")
    column_1 = "Comedy;Mystery;Crime;Drama;Romance;Documentary;Thriller;Action;Animation".split(
        ";"
    )
    column_2 = "Science Fiction;Adventure;War;Horror;Western;Fantasy;Family;History;TV Movie;Music;Foreign".split(
        ";"
    )
    column_names = []
    column_names = column_names + column_0 + column_1 + column_2

    # check has NULL
    for name in column_names:
        has_NA = movies[name].isnull().sum()

        assert has_NA <= 0
        # print(name)
        # print("has null: " + str(has_NA))
        # assert False

    # check no duplicate movieID
    list_movies = movies["movieID"]
    set_movies = set(list_movies)
    assert len(list_movies) == len(set_movies)
    # print("has duplicate!")
    # assert False

    # check binary encode
    # check
    genre = []
    genre = genre + column_1 + column_2
    for name in genre:
        data = movies[name]
        set_data = set(data)
        assert len(set_data) <= 2
        # assert False

    # check length_binned;year_binned TBD
    binned_value = set([0, 1, 2, 3, 4])

    # list_movies = movies["length_binned"]
    # set_movies = set(list_movies)

    # overlap = set_movies.intersection(binned_value)
    # if not len(overlap) == len(set_movies) :
    #     print("length_binned has strange value!")
    #     assert False

    list_movies = movies["year_binned"]
    set_movies = set(list_movies)

    overlap = set_movies.intersection(binned_value)
    assert len(overlap) == len(set_movies)
    # print("length_binned has strange value!")
    # assert False


# check candidates
# They should have vote_average > 6 and popularity > 1
def test_candidates():

    path_to_file = os.path.join(self_dir, "../Datasets/candidates.csv")

    movies = pd.read_csv(path_to_file, sep=",")

    # movies = pd.read_csv("candidates.csv", sep=",")
    v_a = list(movies["vote_average"])
    popular = list(movies["popularity"])
    v_a.sort()
    popular.sort()
    assert v_a[0] > 6.0
    # assert False
    assert popular[0] > 1.0


# check movie data: has Na, has duplicate
def test_data_user():

    path_to_file = os.path.join(self_dir, "../Datasets/data_user.csv")

    movies = pd.read_csv(path_to_file, sep=";")

    # movies = pd.read_csv("data_user.csv", sep=";")
    columns = "userID;age;occupation;gender".split(";")

    for name in columns:
        has_NA = movies[name].isnull().sum()

        assert has_NA <= 0

    ages = list(movies["age"])
    ages.sort()
    assert ages[0] >= 0

    assert ages[-1] < 200

    gender = list(movies["gender"])
    set_gender = set(gender)

    genders = set(["M", "F"])

    assert len(set_gender) == 2 and set_gender.issubset(genders)


# check data_watched.csv
# check NA
# check watchtime is larger than 10
def test_data_watched():

    path_to_file = os.path.join(self_dir, "../Datasets/data_watched.csv")

    movies = pd.read_csv(path_to_file, sep=",")

    # movies = pd.read_csv("data_watched.csv", sep=",")
    columns = list(movies.columns)
    for name in columns:
        has_NA = movies[name].isnull().sum()

        assert has_NA <= 0

    watchTime = list(movies["watchTime"])
    watchTime.sort()

    assert watchTime[0] >= 10


# check data_watched.csv
# check NA
# check watchtime is larger than 10
def test_data():

    path_to_file = os.path.join(self_dir, "../Datasets/data.csv")

    movies = pd.read_csv(path_to_file, sep=",")

    # movies = pd.read_csv("data.csv", sep=",")
    columns = list(movies.columns)
    for name in columns:
        has_NA = movies[name].isnull().sum()

        assert has_NA <= 0

    rating = movies["ratings"]
    set_rating = set(rating)
    rating_value = set([0, 1, 2, 3, 4, 5])
    overlap = set_rating.intersection(rating_value)
    assert len(overlap) == len(set_rating)
    # print("set_rating has strange value!")
    # assert False


def test_watched_rating_1():
    path_to_file = os.path.join(self_dir, "../Datasets/watched_rating_1.csv")

    movies = pd.read_csv(path_to_file, sep=",")
    # movies = pd.read_csv("watched_rating_1.csv", sep=",")
    columns = list(movies.columns)
    for name in columns:
        has_NA = movies[name].isnull().sum()

        assert has_NA <= 0


def test_watched_rating_2():
    path_to_file = os.path.join(self_dir, "../Datasets/watched_rating_2.csv")

    movies = pd.read_csv(path_to_file, sep=",")
    # movies = pd.read_csv("watched_rating_2.csv", sep=",")
    columns = list(movies.columns)
    for name in columns:
        has_NA = movies[name].isnull().sum()

        assert has_NA <= 0
