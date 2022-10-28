import sys

import pandas as pd

sys.path.append("..")


# data.csv is data used for training M1 ALS model. Do not care

# Test rest:
# data_movie_processed.csv is used for M2. Checking for NA, binng age 1 to 5, splitting genre 0 or 1,
# watch_rating_1 and watch_rating_2


def test_data_quality():
    assert True


def test_data_movie_processed():
    print("test_movie_processed")
    try:
        movies = pd.read_csv("data_movie_processed.csv", sep=";")
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

            if has_NA > 0:
                print(name)
                print("has null: " + str(has_NA))
                assert False

        # check no duplicate movieID
        list_movies = movies["movieID"]
        set_movies = set(list_movies)
        if not len(list_movies) == len(set_movies):
            print("has duplicate!")
            assert False

        # check binary encode
        # check
        genre = []
        genre = genre + column_1 + column_2
        for name in genre:
            data = movies[name]
            set_data = set(data)
            if len(set_data) > 2:
                assert False

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
        if not len(overlap) == len(set_movies):
            print("length_binned has strange value!")
            assert False

        assert True
    except Exception:
        assert False


# check candidates
# They should have vote_average > 6 and popularity > 1
def test_candidates():
    movies = pd.read_csv("candidates.csv", sep=",")

    v_a = list(movies["vote_average"])
    popular = list(movies["popularity"])

    v_a.sort()
    popular.sort()

    if not v_a[0] > 6.0:
        assert False

    if not popular[0] > 1.0:
        assert False

    assert True


test_data_movie_processed()
test_candidates()
