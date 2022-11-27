import os
from pathlib import Path

import pandas as pd
import tensorflow as tf

import wandb  # isort:skip
from Models.utils.user_age import binAge  # isort:skip

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

    self_dir = os.path.dirname(__file__)
    path = Path(self_dir)
    my_file = os.path.join(path.parent.absolute(), "sha.txt")

    try:
        with open(my_file, "r") as file:
            actual_version = file.read()
    except FileNotFoundError:
        actual_version = "v0"

    model_version = actual_version
    project_name = "milestone3"

    run = wandb.init(project=project_name)
    model_path = "team-3-comp585/" + project_name + "/retrieval_index:"
    model_version_path = model_path + model_version
    artifact = run.use_artifact(model_version_path, type="model")
    artifact_version = artifact.version
    artifact_dir = os.path.join(
        os.path.join(self_dir, "artifacts"), "retrieval_index-" + str(artifact_version)
    )
    artifact.download(root=artifact_dir)
    wandb.finish()

    model_retrieval_path = artifact_dir
    model_retrieval = tf.saved_model.load(model_retrieval_path)
    print("model retrieval loaded")

    # model_retrieval_path = os.path.join(self_dir, "model_retrieval")
    # model_retrieval = tf.saved_model.load(model_retrieval_path)
    # print("model retrieval loaded")

    movies_path = os.path.join(self_dir, "..", "Datasets", "data_movie_processed.csv")
    movies = pd.read_csv(movies_path, sep=";")
    print("movie features loaded")


init()
