import json
import os
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd  # isort:skip
import tensorflow as tf  # isort:skip
import tensorflow_recommenders as tfrs  # isort:skip
from supabase import create_client  # isort:skip

import wandb  # isort:skip
from kafka_consumer.cloud_database import delete_all_data, get_all_data  # isort:skip

from kafka_consumer.model_utils import create_model  # isort:skip
from kafka_consumer.model_utils import create_tensorflow_datasets  # isort:skip
from kafka_consumer.model_utils import train_test_split  # isort:skip


def movies_preprocessing():
    """
    Load and preprocess the movie dataset in github folder architecture
    :return: Pandas dataframe: the movie data after preprocessing, int: amount of movies we have for training
    """
    movies = pd.read_csv("Datasets/data_movie.csv", sep=",")
    # movie length binned
    bins = [0, 30, 90, 120, 200, 1500]
    labels = [0, 1, 2, 3, 4]
    movies["length_binned"] = pd.cut(movies["length"], bins=bins, labels=labels)
    # year binned
    movies["release_date"] = movies["release_date"].fillna("2000-01-01")  # fill na !!!!
    movies["release_date"] = movies["release_date"].apply(
        lambda row: datetime.strptime(str(row), "%Y-%m-%d").year
    )
    movies["original_language"] = (
        movies["original_language"].fillna("en").astype(str)
    )  # fill na !!!!
    bins = [1850, 1920, 1970, 1990, 2010, 2020, 2025]
    labels = [0, 1, 2, 3, 4, 5]
    movies["year_binned"] = pd.cut(movies["release_date"], bins=bins, labels=labels)
    """
    split the genres from a list of dictionaries to a matrix with columns of genres and rows of movies 1 meaning this
    genre is presented in this movie
    """
    movies["genres"] = movies.apply(lambda row: eval(row["genres"]), axis=1)
    movies["genres"] = movies["genres"].apply(
        lambda row: [d["name"] for d in row if "id" in d]
    )
    # unique_genres = movies["genres"].explode().unique()
    movies = pd.concat(
        [
            movies[
                [
                    "movieID",
                    "length_binned",
                    "year_binned",
                    "vote_average",
                    "popularity",
                    "original_language",
                ]
            ],
            movies.genres.apply(lambda x: pd.Series(1, x)).fillna(0),
        ],
        axis=1,
    )
    N_movies = movies.shape[0]
    return movies, N_movies  # ,unique_genres


def users_preprocessing():
    """
     Load and preprocess the user dataset in github folder architecture
    :return: Pandas dataframe: the user data after preprocessing
    """
    users = pd.read_csv("Datasets/data_user.csv", sep=";")
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = [0, 1, 2, 3, 4, 5, 6]
    users["age_binned"] = pd.cut(users["age"], bins=bins, labels=labels)
    users = users[["userID", "age", "gender", "age_binned", "occupation"]]
    users["userID"] = users["userID"].astype(str)
    return users


def watched_rating_preprocessing(use_ratings_retrieval, watched, ratings):
    """
    Load and preprocess the watched and user dataset in github folder architecture
    :param use_ratings_retrieval: boolean value meaning whether to user ratings value when passing a certain threshold
    as a part of the watched data
    :return: pandas dataframe of the watched data
    """
    # watched = pd.read_csv("../../Datasets/data_watched.csv", sep=",")
    watched["userId"].str.strip()
    watched["userID"] = watched["userId"].astype(str)
    # watched = watched.groupby(['userID', 'movieID'], sort=False, as_index=False)['watchTime'].max()
    watched["movieID"] = watched["movieId"]
    watched = watched[["userID", "movieID"]]
    if use_ratings_retrieval:
        # ratings = pd.read_csv("../../Datasets/data.csv", sep=",")
        ratings["userId"].str.strip()
        ratings["userID"] = ratings["userId"].astype(str)
        ratings["movieID"] = ratings["movieId"]
        ratings = ratings.loc[ratings["rating"] > 3]
        ratings = ratings[["userID", "movieID"]]
        watched = pd.concat([watched, ratings], ignore_index=True)
    return watched


def retrieval_model_data_preprocessing(use_ratings_retrieval, watched, ratings, movies):
    """
    preprocess the data for the retrival model to learn.
    :param use_ratings_retrieval: boolean value meaning whether to user ratings value when passing a certain threshold
    as a part of the watched data
    :return: pandas dataframe of all the required column for retrieval model
    """
    watched = watched_rating_preprocessing(use_ratings_retrieval, watched, ratings)
    users = users_preprocessing()
    watched = watched.merge(movies, left_on="movieID", right_on="movieID", how="left")
    watched = watched.merge(users, left_on="userID", right_on="userID", how="left")
    watched["length_binned"] = watched["length_binned"].fillna(2)
    watched["year_binned"] = watched["year_binned"].fillna(2)
    watched["original_language"] = watched["original_language"].fillna("en")
    watched = watched.drop(["popularity", "vote_average"], axis=1)
    # fill na genres to 0 as not having this genre
    watched = watched.fillna(0)
    watched = watched.drop_duplicates()
    return watched, movies


def data_processing_pipeline(movies):
    API_URL = "https://lsfcmdyggefxunujmnxs.supabase.co"
    key1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxzZmNtZHlnZ2VmeHVudWptbnhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njg0NDczMjYs"
    key2 = "ImV4cCI6MTk4NDAyMzMyNn0.bY-L6ccfEGUK3pc2EeR-EnkWLQTzGvHGskMxXn1f4Uc"
    API_KEY = key1 + key2
    supabase = create_client(API_URL, API_KEY)
    supabase
    rating = get_all_data(supabase, "Rating", None)
    watched = get_all_data(supabase, "WatchTime", None)
    rjson = rating.json()
    rjson = json.loads(rjson)
    rjson = rjson["data"]
    wjson = watched.json()
    wjson = json.loads(wjson)
    wjson = wjson["data"]
    rdf = pd.DataFrame(rjson)
    wdf = pd.DataFrame(wjson)
    pwdf, _ = retrieval_model_data_preprocessing(True, wdf, rdf, movies)
    # deletion for testing it is comment out
    delete_all_data(supabase, "WatchTime")
    delete_all_data(supabase, "Rating")
    return pwdf, rdf, wdf


def data_analysis(run, pwdf, rdf, wdf):
    metadata = pwdf["gender"].value_counts()
    metadata = metadata.to_frame("counts")
    # print(type(metadata))
    metadata = pd.DataFrame.to_dict(metadata)
    preprocssed_artifact = wandb.Artifact(
        "preprocessed", type="dataset", metadata=metadata
    )
    ratings_artifact = wandb.Artifact("ratings", type="dataset")
    watched_artifact = wandb.Artifact("watched", type="dataset")
    tbl1 = wandb.Table(data=pwdf)
    tbl2 = wandb.Table(data=rdf)
    tbl = wandb.Table(data=wdf)
    preprocssed_artifact.add(tbl1, "preprocessed")
    watched_artifact.add(tbl, "watched")
    ratings_artifact.add(tbl2, "ratings")
    run.log_artifact(watched_artifact)
    run.log_artifact(preprocssed_artifact)
    run.log_artifact(ratings_artifact)
    print(metadata)


def model_pipeline(layer_size=32, lr=0.2, epoch=6):
    """
    train the retrieval model defined above with layer_size and cached_train and validate it using the cached_test
    :param cached_train: tensor data used for training
    :param cached_test: tensor data used for validating
    :param layer_size: layer_size for the model
    :param lr: learning rate of the Adam gradient descent
    :version: base model version to be trained
    """
    self_dir = os.path.dirname(__file__)

    movies, _ = movies_preprocessing()
    pwdf, rdf, wdf = data_processing_pipeline(movies)
    print(pwdf.to_string())

    github_sha = os.getenv("APP_SHA")
    project_name = "milestone3"

    run = wandb.init(project=project_name)
    wandb.config.github_sha = github_sha

    data_analysis(run, pwdf, rdf, wdf)

    dataset = pwdf
    N = dataset.shape[0]
    dataset, movies = create_tensorflow_datasets(dataset, movies)
    cached_train, cached_test = train_test_split(dataset, N, seed=42)

    trained_model_artifact = wandb.Artifact(
        "retrieval_model", type="model", description="retrieval trained model"
    )
    index_model_artifact = wandb.Artifact(
        "retrieval_index", type="model", description="index model"
    )
    wandb_callback = wandb.keras.WandbCallback(save_model=True)

    self_dir = os.path.dirname(__file__)
    path = Path(self_dir)
    my_file = os.path.join(path.parent.absolute(), "sha.txt")

    try:
        with open(my_file, "r") as file:
            actual_version = file.read()
    except FileNotFoundError:
        actual_version = "latest"

    new_version = github_sha

    model_path = "team-3-comp585/" + project_name + "/retrieval_model:"
    model_version_path = model_path + actual_version
    artifact = run.use_artifact(model_version_path, type="model")
    artifact_version = artifact.version
    artifact_dir = os.path.join(
        os.path.join(self_dir, "artifacts"), "retrieval_model-" + str(artifact_version)
    )
    artifact.download(root=artifact_dir)

    model_wb = create_model(layer_size)
    model_wb.compile(optimizer=tf.keras.optimizers.legacy.Adagrad(learning_rate=lr))
    weights_path = os.path.join(artifact_dir, "weights_retrieval")
    model_wb.load_weights(weights_path)
    model_wb.fit(cached_train, epochs=epoch, callbacks=[wandb_callback])

    model_dir = os.path.join(self_dir, "model_wb")
    index_dir = os.path.join(self_dir, "index_wb")

    # os.makedirs("Models/model_wb/")
    os.makedirs(model_dir)
    # model_wb.save_weights("Models/model_wb/weights_retrieval", save_format="tf")
    model_wb.save_weights(model_dir + "/weights_retrieval", save_format="tf")
    # os.makedirs("Models/index_wb/")
    os.makedirs(index_dir)
    index = tfrs.layers.factorized_top_k.BruteForce(model_wb.query_model, k=20)
    index.index_from_dataset(
        tf.data.Dataset.zip(
            (
                movies.batch(200).map(lambda x: x["candidate_title"]),
                movies.batch(200).map(model_wb.candidate_model),
            )
        )
    )

    # make a dummy prediction to initialize the model before save it
    user_177165 = {
        "user_age_binned": tf.constant([2]),
        "user_gender": tf.constant([b"M"]),
        "user_id": tf.constant([b"177165"]),
        "user_occupation": tf.constant([b"college/grad student"]),
    }
    _, titles = index(user_177165)

    # tf.saved_model.save(index, "Models/index_wb")
    tf.saved_model.save(index, index_dir)
    # trained_model_artifact.add_dir("Models/model_wb")
    trained_model_artifact.add_dir(model_dir)
    # index_model_artifact.add_dir("Models/index_wb")
    index_model_artifact.add_dir(index_dir)
    run.log_artifact(trained_model_artifact, aliases=[new_version])
    run.log_artifact(index_model_artifact, aliases=[new_version])
    wandb.finish()

    parent_dir = os.path.abspath(os.path.join(self_dir, os.pardir))
    wandb_dir = os.path.join(parent_dir, "wandb")

    shutil.rmtree(model_dir)
    shutil.rmtree(index_dir)
    shutil.rmtree(artifact_dir)
    shutil.rmtree(wandb_dir)


if __name__ == "__main__":
    model_pipeline()
