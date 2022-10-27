import os

import pandas as pd
import tensorflow as tf

from Models.utils.user_age import binAge

self_dir = os.path.dirname(__file__)


def recommendMovies(userID, user_age, user_occupation, user_gender):

    """Get a list of recommended movies for a given user ID, user age, user occupation and user_gender"""
    """Inputs: userID (string), user_age(float), user_occupation(string), user_gender(string)"""

    age_binned = binAge(user_age)

    user = {
        "user_age_binned": tf.constant([age_binned]),
        "user_gender": tf.constant([user_gender]),
        "user_id": tf.constant([userID]),
        "user_occupation": tf.constant([user_occupation]),
    }

    # retrieval candidates
    _, titles = model_retrieval(user)

    # format candidates
    titles_decode = list(titles[0][:].numpy())
    titles_decode = [x.decode("UTF8") for x in titles_decode]

    pred_movies = titles_decode[0:20]

    return pred_movies


def init():
    """Initialize the model"""
    global model_retrieval
    global movies

    model_retrieval_path = os.path.join(self_dir, "model_retrieval")
    model_retrieval = tf.saved_model.load(model_retrieval_path)
    print("model retrieval loaded")

    movies_path = os.path.join(self_dir, "..", "Datasets", "data_movie_processed.csv")
    movies = pd.read_csv(movies_path, sep=";")
    print("movie features loaded")


init()
