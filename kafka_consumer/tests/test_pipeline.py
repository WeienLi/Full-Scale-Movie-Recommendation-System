import sys

# from kafka_consumer.feedback_pipeline import model_pipeline  # isort:skip
from kafka_consumer.feedback_pipeline import movies_preprocessing  # isort:skip
from kafka_consumer.feedback_pipeline import users_preprocessing  # isort:skip
from kafka_consumer.feedback_pipeline import data_processing_pipeline  # isort:skip
from kafka_consumer.model_utils import create_tensorflow_datasets  # isort:skip
from kafka_consumer.model_utils import create_model  # isort:skip

sys.path.append("..")


def test_processing():

    movies, _ = movies_preprocessing()
    assert movies is not None
    pwdf, rdf, wdf = data_processing_pipeline(movies)
    assert pwdf is not None
    assert rdf is not None
    assert wdf is not None

    result = users_preprocessing()
    assert result is not None

    dataset = pwdf
    dataset.shape[0]
    dataset, movies = create_tensorflow_datasets(dataset, movies)
    model = create_model(layer_size=10)
    assert model is not None


# def test_pipeline():
#     try:
#         model_pipeline()
#         assert True
#     except Exception:
#         assert False
