import requests
from flask import Flask, abort
from prometheus_flask_exporter import PrometheusMetrics

from Models.model_inference import recommendMovies

app = Flask(__name__)
# Base URL of the external API for fetching user information
USER_API = "http://fall2022-comp585.cs.mcgill.ca:8080/user/"
DEFAULT_USER = {
    "age": 25,
    "occupation": "other",
    "gender": "M",
}


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
    return ",".join(movies)
