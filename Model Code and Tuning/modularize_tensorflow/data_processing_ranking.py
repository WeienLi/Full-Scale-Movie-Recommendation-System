import numpy as np
import pandas as pd
import sys
from datetime import datetime
import os
import pprint
import tempfile
import data_processing_retrieval


def ratings_preprocessing():
    """
    preprocess the ratings data
    :return: pandas dataframe: ratings data to be used
    """

    ratings = pd.read_csv('../../Datasets/data.csv', sep=',')
    ratings['userID'] = ratings['userID'].astype(str)
    return ratings


def ranking_model_data_processing():
    """
    preprocess all the data and merge them into a single rating dataframe for model to learn
    :return: the pandas dataframe ready to put into tensor
    """
    movies = data_processing_retrieval.movies_preprocessing()
    users = data_processing_retrieval.users_preprocessing()
    ratings = ratings_preprocessing()
    ratings = ratings.merge(movies, left_on='movieID', right_on='movieID', how='left')
    ratings = ratings.merge(users, left_on='userID', right_on='userID', how='left')
    ratings['length_binned'] = ratings['length_binned'].fillna(2)
    ratings['year_binned'] = ratings['year_binned'].fillna(2)
    ratings = ratings.fillna(0)
    ratings = ratings.drop_duplicates()
    ratings['original_language'] = ratings['original_language'].replace(to_replace=0, value="en")
    return ratings

def get_train_test_size(ratings , percentage = 80):
    """
    Compute the lines of data to train and to test
    :param percentage: percentage of data we want to use to train default 80
    :param watched: preprocessed watched pandas dataframe
    :return: N_train: number of data to train, N_test: number of data to test
    """

    N = ratings.shape[0]
    N_train = N * percentage // 100
    N_test = N - N_train
    return N_train, N_test
