from kafka_consumer.model_utils import get_unique_value  # isort:skip
from kafka_consumer.model_utils import train_test_split  # isort:skip
import kafka_consumer.model_utils  # isort:skip

import tensorflow as tf  # isort:skip


def test_get_unique_value():

    get_unique_value(
        ["unique_movie_titles"],
        ["unique_years_binned"],
        ["unique_lengths_binned"],
        ["unique_user_ids"],
        ["unique_user_genders"],
        ["unique_user_ages_binned"],
        ["unique_languages"],
        ["unique_occupations"],
    )
    # not sure how to test something is global
    assert kafka_consumer.model_utils.unique_movie_titles
    assert kafka_consumer.model_utils.unique_years_binned
    assert kafka_consumer.model_utils.unique_lengths_binned
    assert kafka_consumer.model_utils.unique_user_ids
    assert kafka_consumer.model_utils.unique_user_ages_binned
    assert kafka_consumer.model_utils.unique_languages
    assert kafka_consumer.model_utils.unique_occupations

    #  test_train_test_split():

    dataset_list = [i for i in range(200)]
    dataset = tf.data.Dataset.from_tensor_slices(dataset_list)
    train, test = train_test_split(dataset, 50, 42)
    assert train is not None
    assert test is not None
