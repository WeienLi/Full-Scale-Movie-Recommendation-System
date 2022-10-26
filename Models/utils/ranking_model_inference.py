from typing import Dict, Text

import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs


class RankingModel(tf.keras.Model):
    def __init__(self):
        super().__init__()
        embedding_dimension = 32

        # Compute embeddings for users.
        self.user_embeddings = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_user_ids, mask_token=None
                ),
                tf.keras.layers.Embedding(
                    len(unique_user_ids) + 1, embedding_dimension
                ),
            ]
        )

        # Compute embeddings for movies.
        self.movie_embeddings = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_movie_titles, mask_token=None
                ),
                tf.keras.layers.Embedding(
                    len(unique_movie_titles) + 1, embedding_dimension
                ),
            ]
        )

        # users features
        self.age_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.IntegerLookup(
                    vocabulary=unique_user_ages_binned, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_user_ages_binned) + 1, 8),
            ]
        )

        self.gender_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_user_genders, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_user_genders) + 1, 8),
            ]
        )

        self.occupation_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_occupations, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_occupations) + 1, 8),
            ]
        )

        # movie features

        self.lenght_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.IntegerLookup(
                    vocabulary=unique_lengths_binned, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_lengths_binned) + 1, 8),
            ]
        )

        self.year_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.IntegerLookup(
                    vocabulary=unique_years_binned, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_years_binned) + 1, 8),
            ]
        )

        self.language_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_languages, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_languages) + 1, 8),
            ]
        )

        self.genre_embedding = tf.keras.layers.Dense(32)

        # Compute predictions.
        self.ratings = tf.keras.Sequential(
            [
                # Learn multiple dense layers.
                tf.keras.layers.Dense(256, activation="relu"),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dense(32, activation="relu"),
                # Make rating predictions in the final layer.
                tf.keras.layers.Dense(1),
            ]
        )

    def call(self, inputs):
        # user_id, movie_title = inputs

        Comedy = tf.expand_dims(inputs["candidate_Comedy"], axis=1)
        Mystery = tf.expand_dims(inputs["candidate_Mystery"], axis=1)
        Crime = tf.expand_dims(inputs["candidate_Crime"], axis=1)
        Drama = tf.expand_dims(inputs["candidate_Drama"], axis=1)
        Romance = tf.expand_dims(inputs["candidate_Romance"], axis=1)
        Documentary = tf.expand_dims(inputs["candidate_Documentary"], axis=1)
        Thriller = tf.expand_dims(inputs["candidate_Thriller"], axis=1)
        Action = tf.expand_dims(inputs["candidate_Action"], axis=1)
        Animation = tf.expand_dims(inputs["candidate_Animation"], axis=1)
        Science_Fiction = tf.expand_dims(inputs["candidate_Science_Fiction"], axis=1)
        Adventure = tf.expand_dims(inputs["candidate_Adventure"], axis=1)
        War = tf.expand_dims(inputs["candidate_War"], axis=1)
        Horror = tf.expand_dims(inputs["candidate_Horror"], axis=1)
        Western = tf.expand_dims(inputs["candidate_Western"], axis=1)
        Fantasy = tf.expand_dims(inputs["candidate_Fantasy"], axis=1)
        Family = tf.expand_dims(inputs["candidate_Family"], axis=1)
        History = tf.expand_dims(inputs["candidate_History"], axis=1)
        TV_Movie = tf.expand_dims(inputs["candidate_TV_Movie"], axis=1)
        Music = tf.expand_dims(inputs["candidate_Music"], axis=1)
        Foreign = tf.expand_dims(inputs["candidate_Foreign"], axis=1)

        genres = tf.concat(
            values=[
                Comedy,
                Mystery,
                Crime,
                Drama,
                Romance,
                Documentary,
                Thriller,
                Action,
                Animation,
                Science_Fiction,
                Adventure,
                War,
                Horror,
                Western,
                Fantasy,
                Family,
                History,
                TV_Movie,
                Music,
                Foreign,
            ],
            axis=1,
        )

        user_embedding = self.user_embeddings(inputs["user_id"])
        movie_embedding = self.movie_embeddings(inputs["movie_title"])
        age_embedding = self.age_embedding(inputs["user_age_binned"])
        gender_embedding = self.gender_embedding(inputs["user_gender"])
        occupation_embedding = self.occupation_embedding(inputs["user_occupation"])
        lenght_embedding = self.lenght_embedding(inputs["movie_length_binned"])
        year_embedding = self.year_embedding(inputs["movie_year_binned"])
        genre_embedding = self.genre_embedding(genres)
        language_embedding = self.language_embedding(inputs["movie_language"])

        return self.ratings(
            tf.concat(
                [
                    user_embedding,
                    movie_embedding,
                    age_embedding,
                    gender_embedding,
                    occupation_embedding,
                    lenght_embedding,
                    year_embedding,
                    genre_embedding,
                    language_embedding,
                ],
                axis=1,
            )
        )


class RecRankModel(tfrs.models.Model):
    def __init__(self):
        super().__init__()
        self.ranking_model: tf.keras.Model = RankingModel()
        self.task: tf.keras.layers.Layer = tfrs.tasks.Ranking(
            loss=tf.keras.losses.MeanSquaredError(),
            metrics=[tf.keras.metrics.RootMeanSquaredError()],
        )

    def call(self, features: Dict[str, tf.Tensor]) -> tf.Tensor:
        return self.ranking_model(
            {
                "user_id": features["user_id"],
                "movie_title": features["movie_title"],
                "user_age_binned": features["user_age_binned"],
                "user_gender": features["user_gender"],
                "user_occupation": features["user_occupation"],
                "movie_language": features["movie_language"],
                "movie_length_binned": features["movie_length_binned"],
                "movie_year_binned": features["movie_year_binned"],
                "candidate_Comedy": features["comedy"],
                "candidate_Mystery": features["mystery"],
                "candidate_Crime": features["crime"],
                "candidate_Drama": features["drama"],
                "candidate_Romance": features["romance"],
                "candidate_Documentary": features["documentary"],
                "candidate_Thriller": features["thriller"],
                "candidate_Action": features["action"],
                "candidate_Animation": features["animation"],
                "candidate_Science_Fiction": features["science_fiction"],
                "candidate_Adventure": features["adventure"],
                "candidate_War": features["war"],
                "candidate_Horror": features["horror"],
                "candidate_Western": features["western"],
                "candidate_Fantasy": features["fantasy"],
                "candidate_Family": features["family"],
                "candidate_History": features["history"],
                "candidate_TV_Movie": features["tv_movie"],
                "candidate_Music": features["music"],
                "candidate_Foreign": features["foreign"],
            }
        )

    def compute_loss(
        self, features: Dict[Text, tf.Tensor], training=False
    ) -> tf.Tensor:
        labels = features.pop("user_rating")

        rating_predictions = self(features)

        # The task computes the loss and the metrics.
        return self.task(labels=labels, predictions=rating_predictions)


def get_model(path="utils/unique_values/"):

    global unique_movie_titles
    global unique_years_binned
    global unique_lengths_binned
    global unique_user_ids
    global unique_user_genders
    global unique_user_ages_binned
    global unique_languages
    global unique_occupations

    unique_movie_titles = list(np.loadtxt(path + "unique_movie_titles.txt", dtype=str))
    unique_years_binned = list(
        np.loadtxt(path + "unique_years_binned.txt", dtype=float)
    )
    unique_lengths_binned = list(
        np.loadtxt(path + "unique_lengths_binned.txt", dtype=float)
    )
    unique_user_ids = list(np.loadtxt(path + "unique_user_ids.txt", dtype=str))
    unique_user_genders = list(np.loadtxt(path + "unique_user_genders.txt", dtype=str))
    unique_user_ages_binned = list(
        np.loadtxt(path + "unique_user_ages_binned.txt", dtype=float)
    )
    unique_languages = list(np.loadtxt(path + "unique_languages.txt", dtype=str))
    unique_occupations = list(
        np.loadtxt(path + "unique_occupations.txt", delimiter="\n", dtype=str)
    )

    model = RecRankModel()

    return model
