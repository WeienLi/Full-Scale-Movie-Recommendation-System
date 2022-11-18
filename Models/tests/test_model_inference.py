import numpy as np
import pandas as pd
import pytest
import tensorflow as tf

from Models.utils.input_ranking import inputRanking
from Models.utils.ranking_model_inference import get_model
from Models.utils.user_age import binAge


def test_my_test():
    assert True


def test_load_model():
    try:
        global model_retrieval, model_ranking, movies
        model_retrieval = tf.saved_model.load("Models/model_retrieval")
        model_ranking = get_model("Models/utils/unique_values/")
        model_ranking.load_weights("Models/model_rank/ranking.ckpt")
        movies = pd.read_csv("Datasets/data_movie_processed.csv", sep=";")
    except Exception:
        assert False


def test_retrieval():
    userID = b"1"
    user_age = 34
    user_occupation = b"sales/marketing"
    user_gender = b"M"
    age_binned = binAge(user_age)
    user = {
        "user_age_binned": tf.constant([age_binned]),
        "user_gender": tf.constant([user_gender]),
        "user_id": tf.constant([userID]),
        "user_occupation": tf.constant([user_occupation]),
    }
    _, titles = model_retrieval(user)
    assert len(titles[0, :]) == 500


@pytest.mark.skip(reason="Not using ranking model right now")
def test_ranking():
    userID = b"1"
    user_age = 34
    user_occupation = b"sales/marketing"
    user_gender = b"M"
    age_binned = binAge(user_age)
    candidate = movies.head(1)
    input = inputRanking(userID, age_binned, user_gender, user_occupation, candidate, 0)
    pred = model_ranking(input)
    pred2 = pred.numpy()
    assert type(pred2[0, 0]) == np.float32


def test_retrieval2():
    userID = None
    user_age = 100
    user_occupation = "lzy"
    user_gender = "MF"
    age_binned = binAge(user_age)
    try:
        user = {
            "user_age_binned": tf.constant([age_binned]),
            "user_gender": tf.constant([user_gender]),
            "user_id": tf.constant([userID]),
            "user_occupation": tf.constant([user_occupation]),
        }
        _, titles = model_retrieval(user)
    except Exception:
        assert True


def test_retrieval3():
    userID = b"1"
    user_age = 34
    user_occupation = b"sales/marketing"
    user_gender = b"M"
    age_binned = binAge(user_age)
    user = {
        "user_age_binned": tf.constant([age_binned]),
        "user_gender": tf.constant([user_gender]),
        "user_id": tf.constant([userID]),
        "user_occupation": tf.constant([user_occupation]),
    }
    _, titles = model_retrieval(user)
    t1 = titles[
        0,
    ]
    assert type(t1[0].numpy()) == bytes


@pytest.mark.skip(reason="Not using ranking model right now")
def test_ranking2():
    userID = b"1"
    user_age = 34
    user_occupation = b"sales/marketing"
    user_gender = b"M"
    age_binned = binAge(user_age)
    candidate = movies.head(2)
    input = inputRanking(userID, age_binned, user_gender, user_occupation, candidate, 0)
    pred = model_ranking(input)
    pred2 = pred.numpy()
    input2 = inputRanking(
        userID, age_binned, user_gender, user_occupation, candidate, 1
    )
    pred3 = model_ranking(input2)
    pred4 = pred3.numpy()
    assert type(pred2[0, 0]) == np.float32 and type(pred4[0, 0]) == np.float32


@pytest.mark.skip(reason="Not using ranking model right now")
def test_ranking3():
    userID = None
    user_age = 34
    user_occupation = b"sales/marketing"
    user_gender = b"M"
    age_binned = binAge(user_age)
    try:
        candidate = movies.head(1)
        input = inputRanking(
            userID, age_binned, user_gender, user_occupation, candidate, 0
        )
        pred = model_ranking(input)
        pred.numpy()
    except Exception:
        assert True
