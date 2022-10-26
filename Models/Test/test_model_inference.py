import pytest
import json
import os
import sys

import tensorflow as tf
import tensorflow_recommenders as tfrs
import numpy as np
import pandas as pd
from Models.utils.ranking_model_inference import get_model
from Models.utils.user_age import binAge
from Models.utils.input_ranking import inputRanking
def test_my_test():
    assert True


def test_load_model():
    try:
        global model_retrieval,model_ranking,movies
        model_retrieval =  tf.saved_model.load('../model_retrieval')
        model_ranking = get_model('../utils/unique_values/')
        model_ranking.load_weights("../model_rank/ranking.ckpt")
        #print(type(model_ranking))
        #print(type(model_retrieval))
        movies = pd.read_csv('../../Datasets/data_movie_processed.csv', sep=';')
    except Exception as exc:
        assert False

def test_retrieval():
    userID = b'1'
    user_age = 34
    user_occupation = b'sales/marketing'
    user_gender = b'M'
    age_binned = binAge(user_age)
    user = {
        'user_age_binned': tf.constant([age_binned]),
        'user_gender': tf.constant([user_gender]) ,
        'user_id': tf.constant([userID]),
        'user_occupation': tf.constant([user_occupation]) }
    _,titles = model_retrieval(user)
    assert len(titles[0,]) == 500

def test_ranking():
    userID = b'1'
    user_age = 34
    user_occupation = b'sales/marketing'
    user_gender = b'M'
    age_binned = binAge(user_age)
    candidate = movies.head(1)
    input = inputRanking(userID, age_binned, user_gender, user_occupation, candidate, 0)
    pred = model_ranking(input)
    pred2 = pred.numpy()
    assert type(pred2[0,0]) == np.float32

def test_retrieval2():
    userID = None
    user_age = 100
    user_occupation = 'lzy'
    user_gender = 'MF'
    age_binned = binAge(user_age)
    try:
        user = {
            'user_age_binned': tf.constant([age_binned]),
            'user_gender': tf.constant([user_gender]) ,
            'user_id': tf.constant([userID]),
            'user_occupation': tf.constant([user_occupation]) }
        _,titles = model_retrieval(user)
    except Exception as exc:
        assert True

def test_retrieval3():
    userID = b'1'
    user_age = 34
    user_occupation = b'sales/marketing'
    user_gender = b'M'
    age_binned = binAge(user_age)
    user = {
        'user_age_binned': tf.constant([age_binned]),
        'user_gender': tf.constant([user_gender]) ,
        'user_id': tf.constant([userID]),
        'user_occupation': tf.constant([user_occupation]) }
    _,titles = model_retrieval(user)
    t1 = titles[0,]
    print(t1[0].numpy())
    assert type(t1[0].numpy()) == bytes

def test_ranking2():
    userID = b'1'
    user_age = 34
    user_occupation = b'sales/marketing'
    user_gender = b'M'
    age_binned = binAge(user_age)
    candidate = movies.head(2)
    input = inputRanking(userID, age_binned, user_gender, user_occupation, candidate, 0)
    pred = model_ranking(input)
    pred2 = pred.numpy()
    input2 = inputRanking(userID, age_binned, user_gender, user_occupation, candidate, 1)
    pred3 = model_ranking(input2)
    pred4 = pred3.numpy()
    assert type(pred2[0,0]) == np.float32 and type(pred4[0,0]) == np.float32

def test_ranking3():
    userID = None
    user_age = 34
    user_occupation = b'sales/marketing'
    user_gender = b'M'
    age_binned = binAge(user_age)
    try:
        candidate = movies.head(1)
        input = inputRanking(userID, age_binned, user_gender, user_occupation, candidate, 0)
        pred = model_ranking(input)
        pred2 = pred.numpy()
    except Exception as exc:
        assert True
