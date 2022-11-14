import os
import time

import requests
from flask import Flask, abort
from prometheus_flask_exporter import PrometheusMetrics

from Database.db import RedisDB
from Models.model_inference import recommendMovies

from .constants import APP_MODES, SavedRec

app = Flask(__name__)
db = RedisDB()

# Base URL of the external API for fetching user information
USER_API = "http://fall2022-comp585.cs.mcgill.ca:8080/user/"
DEFAULT_USER = {
    "age": 25,
    "occupation": "other",
    "gender": "M",
}
APP_MODE = os.environ.get("APP_MODE", APP_MODES.CANARY)


def metrics_rule(req):
    if req.path == "/":
        return req.path
    return "/" + req.path.split("/")[1]


metrics = PrometheusMetrics(app, group_by=metrics_rule)
metrics.info("app_info", "Monitoring flask API", version="1.0.0")


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/recommend/<userID>", methods=["GET"])
def getRecommendations(userID):
    """Get a list of recommended movies for a given user ID"""
    """Inputs: userID (string)"""
    # check if recommendations are already in cache
    db_key_prefix = ""
    if APP_MODE == str(APP_MODES.CANARY.value):
        db_key_prefix = "canary:"

    data = db.get(db_key_prefix + userID)
    if data is not None:
        db.execute_command("TS.INCRBY", db_key_prefix + "cache:hit", 1)
        parsed_data = SavedRec(data)
        return parsed_data.recommendations
    else:
        db.execute_command("TS.INCRBY", db_key_prefix + "cache:miss", 1)

    # get user information from API
    user = DEFAULT_USER
    try:
        r = requests.get(USER_API + userID)
        user_info = r.json()
        if user_info["age"] is not None:
            age = user_info["age"]
            try:
                user["age"] = int(age)
            except ValueError:
                print("Could not convert user's age (" + age + ") to int.")

        if user_info["occupation"] is not None:
            user["occupation"] = user_info["occupation"]

        if user_info["gender"] is not None:
            user["gender"] = user_info["gender"]
    except Exception as e:
        print("Could not get user information from API: " + str(e))
        abort(404, "User not found")

    # get recommendations
    print("Getting recommendations for user " + userID)
    movies = recommendMovies(userID, user["age"], user["occupation"], user["gender"])
    result = ",".join(movies)

    # cache recommendations
    saved_rec = SavedRec()
    sha = os.environ.get("GITHUB_SHA", "unknown")
    saved_rec.init(userID, result, time.time(), sha, str(APP_MODE))
    db.set(db_key_prefix + userID, str(saved_rec))

    return result


@app.after_request
def show_app_mode(response):
    response.headers["App-Mode"] = APP_MODE
    response.headers["Github-SHA"] = os.environ.get("GITHUB_SHA", "unknown")
    return response
