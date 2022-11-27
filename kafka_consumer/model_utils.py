import numpy as np
import tensorflow as tf
import tensorflow_recommenders as tfrs


def train_test_split(dataset, N, seed=42):
    """
    splitting the tensor dataset to cached training and testing
    :param N_train: number of training data we would like
    :param N_test: number of testing data we would like
    :param seed: the seed we want to use for random default 42
    :return: the cached training and testing data
    """

    N_train = N * 80 // 100
    N_test = N - N_train

    tf.random.set_seed(seed)
    shuffled = dataset.shuffle(N, seed=seed, reshuffle_each_iteration=False)

    train = shuffled.take(N_train)
    test = shuffled.skip(N_train).take(N_test)

    cached_train = train.shuffle(N_train).batch(64).cache()  # 8192
    cached_test = test.batch(64).cache()
    return cached_train, cached_test


def get_unique_value(
    unique_movie_titles1,
    unique_years_binned1,
    unique_lengths_binned1,
    unique_user_ids1,
    unique_user_genders1,
    unique_user_ages_binned1,
    unique_languages1,
    unique_occupations1,
):
    global unique_movie_titles
    global unique_years_binned
    global unique_lengths_binned
    global unique_user_ids
    global unique_user_genders
    global unique_user_ages_binned
    global unique_languages
    global unique_occupations
    unique_movie_titles = unique_movie_titles1
    unique_years_binned = unique_years_binned1
    unique_lengths_binned = unique_lengths_binned1
    unique_user_ids = unique_user_ids1
    unique_user_genders = unique_user_genders1
    unique_user_ages_binned = unique_user_ages_binned1
    unique_languages = unique_languages1
    unique_occupations = unique_occupations1


def create_tensorflow_datasets(watched_i, movies_i):
    """
    Converting dataframe of pandas to tensorflow datasets for the model to use
    :param watched: preprocessed pandas dataframe of the watched datasets
    :param movies: preprocessed movies dataframe of the watched datasets
    :return: watched and movies in tensorflow_datasets
    """
    global watched, movies
    watched = tf.data.Dataset.from_tensor_slices(dict(watched_i))
    movies = tf.data.Dataset.from_tensor_slices(dict(movies_i))
    watched = watched.map(
        lambda x: {
            "movie_title": x["movieID"],
            "movie_length_binned": x["length_binned"],
            "movie_year_binned": x["year_binned"],
            "movie_language": x["original_language"],
            "user_id": x["userID"],
            "user_gender": x["gender"],
            "user_age_binned": x["age_binned"],
            "user_occupation": x["occupation"],
            "Comedy": x["Comedy"],
            "Mystery": x["Mystery"],
            "Crime": x["Crime"],
            "Drama": x["Drama"],
            "Romance": x["Romance"],
            "Documentary": x["Documentary"],
            "Thriller": x["Thriller"],
            "Action": x["Action"],
            "Animation": x["Animation"],
            "Science Fiction": x["Science Fiction"],
            "Adventure": x["Adventure"],
            "War": x["War"],
            "Horror": x["Horror"],
            "Western": x["Western"],
            "Fantasy": x["Fantasy"],
            "Family": x["Family"],
            "History": x["History"],
            "TV Movie": x["TV Movie"],
            "Music": x["Music"],
            "Foreign": x["Foreign"],
        }
    )
    movies = movies.map(
        lambda x: {
            "candidate_title": x["movieID"],
            "candidate_length_binned": x["length_binned"],
            "candidate_year_binned": x["year_binned"],
            "candidate_language": x["original_language"],
            "candidate_Comedy": x["Comedy"],
            "candidate_Mystery": x["Mystery"],
            "candidate_Crime": x["Crime"],
            "candidate_Drama": x["Drama"],
            "candidate_Romance": x["Romance"],
            "candidate_Documentary": x["Documentary"],
            "candidate_Thriller": x["Thriller"],
            "candidate_Action": x["Action"],
            "candidate_Animation": x["Animation"],
            "candidate_Science_Fiction": x["Science Fiction"],
            "candidate_Adventure": x["Adventure"],
            "candidate_War": x["War"],
            "candidate_Horror": x["Horror"],
            "candidate_Western": x["Western"],
            "candidate_Fantasy": x["Fantasy"],
            "candidate_Family": x["Family"],
            "candidate_History": x["History"],
            "candidate_TV_Movie": x["TV Movie"],
            "candidate_Music": x["Music"],
            "candidate_Foreign": x["Foreign"],
        }
    )
    return watched, movies


class RetrievalUserModel(tf.keras.Model):
    def __init__(self, layer_sizes):
        super().__init__()

        self.user_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_user_ids, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_user_ids) + 1, 32),
            ]
        )

        self.age_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.IntegerLookup(
                    vocabulary=unique_user_ages_binned, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_user_ages_binned) + 1, 4),
            ]
        )

        self.gender_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_user_genders, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_user_genders) + 1, 1),
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

        # Then construct the layers.
        self.dense_layers = tf.keras.Sequential()

        # Use the ReLU activation for all but the last layer.
        for layer_size in layer_sizes[:-1]:
            # self.dense_layers.add(tf.keras.layers.Dropout(0.2, (layer_size,)))
            self.dense_layers.add(
                tf.keras.layers.Dense(
                    layer_size, kernel_regularizer="l2", activation="relu"
                )
            )

        # No activation for the last layer.
        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size))

    def call(self, inputs):

        feature_embedding = tf.concat(
            values=[
                self.user_embedding(inputs["user_id"]),
                self.age_embedding(inputs["user_age_binned"]),
                self.gender_embedding(inputs["user_gender"]),
                self.occupation_embedding(inputs["user_occupation"]),
            ],
            axis=1,
        )
        return self.dense_layers(feature_embedding)


class RetrievalMovieModel(tf.keras.Model):
    def __init__(self, layer_sizes):

        super().__init__()

        self.title_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_movie_titles, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_movie_titles) + 1, 32),
            ]
        )

        self.lenght_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.IntegerLookup(
                    vocabulary=unique_lengths_binned, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_lengths_binned) + 1, 2),
            ]
        )

        self.year_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.IntegerLookup(
                    vocabulary=unique_years_binned, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_years_binned) + 1, 2),
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

        self.genre_embedding = tf.keras.layers.Dense(4, activation="relu")

        # Then construct the layers.
        self.dense_layers = tf.keras.Sequential()

        # Use the ReLU activation for all but the last layer.
        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(
                tf.keras.layers.Dense(
                    layer_size, kernel_regularizer="l2", activation="relu"
                )
            )

        # No activation for the last layer.
        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size))

    def call(self, inputs):

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

        feature_embedding = tf.concat(
            values=[
                self.title_embedding(inputs["candidate_title"]),
                self.lenght_embedding(inputs["candidate_length_binned"]),
                self.year_embedding(inputs["candidate_year_binned"]),
                self.genre_embedding(genres),
                self.language_embedding(inputs["candidate_language"]),
            ],
            axis=1,
        )
        return self.dense_layers(feature_embedding)


class RecRetModel(tfrs.Model):
    def __init__(self, layer_sizes):
        super().__init__()

        self.query_model = tf.keras.Sequential(
            [RetrievalUserModel(layer_sizes), tf.keras.layers.Dense(32)]
        )

        self.candidate_model = tf.keras.Sequential(
            [RetrievalMovieModel(layer_sizes), tf.keras.layers.Dense(32)]
        )

        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=movies.batch(30000).map(self.candidate_model),
                ks=(5, 20, 500),
            ),
        )

    def compute_loss(self, features, training=False):

        query_embeddings = self.query_model(
            {
                "user_id": features["user_id"],
                "user_age_binned": features["user_age_binned"],
                "user_gender": features["user_gender"],
                "user_occupation": features["user_occupation"],
                "movie_length_binned": features["movie_length_binned"],
                "movie_year_binned": features["movie_year_binned"],
                "movie_language": features["movie_language"],
            }
        )

        movie_embeddings = self.candidate_model(
            {
                "candidate_title": features["movie_title"],
                "candidate_length_binned": features["movie_length_binned"],
                "candidate_year_binned": features["movie_year_binned"],
                "candidate_language": features["movie_language"],
                "candidate_Comedy": features["Comedy"],
                "candidate_Mystery": features["Mystery"],
                "candidate_Crime": features["Crime"],
                "candidate_Drama": features["Drama"],
                "candidate_Romance": features["Romance"],
                "candidate_Documentary": features["Documentary"],
                "candidate_Thriller": features["Thriller"],
                "candidate_Action": features["Action"],
                "candidate_Animation": features["Animation"],
                "candidate_Science_Fiction": features["Science Fiction"],
                "candidate_Adventure": features["Adventure"],
                "candidate_War": features["War"],
                "candidate_Horror": features["Horror"],
                "candidate_Western": features["Western"],
                "candidate_Fantasy": features["Fantasy"],
                "candidate_Family": features["Family"],
                "candidate_History": features["History"],
                "candidate_TV_Movie": features["TV Movie"],
                "candidate_Music": features["Music"],
                "candidate_Foreign": features["Foreign"],
            }
        )

        return self.task(query_embeddings, movie_embeddings)


def create_model(layer_size):

    path = "Models/utils/unique_values/"
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

    get_unique_value(
        unique_movie_titles,
        unique_years_binned,
        unique_lengths_binned,
        unique_user_ids,
        unique_user_genders,
        unique_user_ages_binned,
        unique_languages,
        unique_occupations,
    )

    return RecRetModel([layer_size])
