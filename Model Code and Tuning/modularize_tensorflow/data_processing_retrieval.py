import numpy as np
import pandas as pd
import sys
from datetime import datetime
import os
import pprint
import tempfile

def movies_preprocessing():
    """
    Load and preprocess the movie dataset in github folder architecture
    :return: Pandas dataframe: the movie data after preprocessing, int: amount of movies we have for training
    """
    movies = pd.read_csv('../../Datasets/data_movie.csv', sep=',')
    #movie length binned
    bins = [0, 30, 90, 120, 200, 1500]
    labels = [0, 1, 2, 3, 4]
    movies['length_binned'] = pd.cut(movies['length'], bins=bins, labels=labels)
    # year binned
    movies['release_date'] = movies['release_date'].fillna('2000-01-01')  # fill na !!!!
    movies['release_date'] = movies['release_date'].apply(lambda row: datetime.strptime(str(row), '%Y-%m-%d').year)
    movies['original_language'] = movies['original_language'].fillna("en").astype(str)  # fill na !!!!
    bins = [1850, 1920, 1970, 1990, 2010, 2020, 2025]
    labels = [0, 1, 2, 3, 4, 5]
    movies['year_binned'] = pd.cut(movies['release_date'], bins=bins, labels=labels)
    """
    split the genres from a list of dictionaries to a matrix with columns of genres and rows of movies 1 meaning this
    genre is presented in this movie
    """
    movies['genres'] = movies.apply(lambda row: eval(row['genres']), axis=1)
    movies['genres'] = movies['genres'].apply(lambda row: [d['name'] for d in row if 'id' in d])
    #unique_genres = movies["genres"].explode().unique()
    movies = pd.concat([
        movies[['movieID', 'length_binned', 'year_binned', 'vote_average', 'popularity', 'original_language']],
        movies.genres.apply(lambda x: pd.Series(1, x)).fillna(0)
    ], axis=1)
    N_movies = movies.shape[0]
    return movies,N_movies #,unique_genres

def users_preprocessing():
    """
     Load and preprocess the user dataset in github folder architecture
    :return: Pandas dataframe: the user data after preprocessing
    """
    users = pd.read_csv('../../Datasets/user_data.csv', sep=';')
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = [0, 1, 2, 3, 4, 5, 6]
    users['age_binned'] = pd.cut(users['age'], bins=bins, labels=labels)
    users = users[['userID', 'age', 'gender', 'age_binned', 'occupation']]
    users['userID'] = users['userID'].astype(str)
    return users

def watched_rating_preprocessing(use_ratings_retrieval):
    """
    Load and preprocess the watched and user dataset in github folder architecture
    :param use_ratings_retrieval: boolean value meaning whether to user ratings value when passing a certain threshold
    as a part of the watched data
    :return: pandas dataframe of the watched data
    """
    watched = pd.read_csv('../../Datasets/data_watched.csv', sep=',')
    watched['userID'] = watched['userID'].astype(str)
    #watched = watched.groupby(['userID', 'movieID'], sort=False, as_index=False)['watchTime'].max()
    watched = watched[['userID', 'movieID']]
    if use_ratings_retrieval:
        ratings = pd.read_csv('../../Datasets/data.csv', sep=',')
        ratings['userID'] = ratings['userID'].astype(str)
        ratings = ratings.loc[ratings['ratings'] > 3]
        ratings = ratings[['userID', 'movieID']]
        watched = pd.concat([watched, ratings], ignore_index=True)
    return watched

def retrieval_model_data_preprocessing(use_ratings_retrieval):
    """
    preprocess the data for the retrival model to learn.
    :param use_ratings_retrieval: boolean value meaning whether to user ratings value when passing a certain threshold
    as a part of the watched data
    :return: pandas dataframe of all the required column for retrieval model
    """
    watched = watched_rating_preprocessing(use_ratings_retrieval)
    users = users_preprocessing()
    movies = movies_preprocessing()
    watched = watched.merge(movies, left_on='movieID', right_on='movieID', how='left')
    watched = watched.merge(users, left_on='userID', right_on='userID', how='left')
    watched['length_binned'] = watched['length_binned'].fillna(2)
    watched['year_binned'] = watched['year_binned'].fillna(2)
    watched['original_language'] = watched['original_language'].fillna('en')
    watched = watched.drop(['popularity', 'vote_average'], axis=1)
    #fill na genres to 0 as not having this genre
    watched = watched.fillna(0)
    watched = watched.drop_duplicates()
    return watched,movies

def cut_candidates(movies):
    movies = movies.loc[movies['vote_average'] > 6]
    movies = movies.loc[movies['popularity'] > 1]
    return movies

def get_train_test_size(watched , percentage = 80):
    """
    Compute the lines of data to train and to test
    :param percentage: percentage of data we want to use to train default 80
    :param watched: preprocessed watched pandas dataframe
    :return: N_train: number of data to train, N_test: number of data to test
    """
    N = watched.shape[0]
    N_train = N * percentage // 100
    N_test = N - N_train
    return N_train, N_test
