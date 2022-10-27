import os
import pprint
import tempfile
import time

from typing import Dict, Text

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

import tensorflow_recommenders as tfrs
import pandas as pd
import sys
from datetime import datetime
import data_processing_retrieval
import retrieval_model

def Countinous_Learning():
    #global watched
    #global movies
    """
    global unique_movie_titles
    global unique_years_binned
    global unique_lengths_binned
    global unique_user_ids
    global unique_user_genders
    global unique_user_ages_binned
    global unique_languages
    global unique_occupations
    """
    #wat1 = pd.read_csv('../../Datasets/watched_rating_1.csv')
    #wat2 = pd.read_csv('../../Datasets/watched_rating_2.csv')
    movies = pd.read_csv('../../Datasets/candidates.csv')
    #movies = pd.read_csv('../../Datasets/data_movie_processed.csv',sep=';')
    #watched = pd.concat([wat1, wat2])
    watched = pd.read_csv('../../Datasets/watched_rating_1.csv')
    watched = watched.iloc[:30000,]
    watched['userID'] = watched['userID'].astype(str)
    watched = watched.drop(columns=['Unnamed: 0'])
    N,N_train, N_test = data_processing_retrieval.get_train_test_size(watched)
    watched, movies = retrieval_model.create_tensorflow_datasets(watched, movies)
    cached_train,cached_test = retrieval_model.train_test_split(N, N_train, N_test, seed=42)

    path = '../../Models/utils/unique_values/'
    unique_movie_titles = list(np.loadtxt(path + 'unique_languages.txt', dtype=str))
    unique_years_binned = list(np.loadtxt(path + "unique_years_binned.txt", dtype=float))
    unique_lengths_binned = list(np.loadtxt(path + "unique_lengths_binned.txt", dtype=float))
    unique_user_ids = list(np.loadtxt(path + "unique_user_ids.txt", dtype=str))
    unique_user_genders = list(np.loadtxt(path + "unique_user_genders.txt", dtype=str))
    unique_user_ages_binned = list(np.loadtxt(path + "unique_user_ages_binned.txt", dtype=float))
    unique_languages = list(np.loadtxt(path + "unique_languages.txt", dtype=str))
    unique_occupations = list(np.loadtxt(path + "unique_occupations.txt", delimiter="\n", dtype=str))
    retrieval_model.get_unique_value(unique_movie_titles,unique_years_binned,unique_lengths_binned,unique_user_ids,
                                     unique_user_genders,unique_user_ages_binned,unique_languages,unique_occupations)
    #print("Hello")
    retrieval_model.train_retrieval(True,cached_train,cached_test,16,0.006,2)


st = time.time()
Countinous_Learning()
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
