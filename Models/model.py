import json
import os


def recommendMovies(userID):
    """Get a list of recommended movies for a given user ID"""
    # Return a pre-defined (random) result if the user ID is not in the recommendations
    if userID not in recommendations:
        userID = 0

    rec_list = recommendations[str(userID)]
    # return the movie titles
    return [lookup[str(movieID)] for movieID in rec_list]


def init():
    """Initialize the model"""
    global lookup
    global recommendations
    # load the cached recommendations JSON
    root = os.path.join(os.path.dirname(__file__))
    with open(os.path.join(root, "cache", "recommendations.json"), "r") as f:
        recommendations = json.load(f)

    with open(os.path.join(root, "cache", "lookuptable.json"), "r") as f:
        lookup = json.load(f)

    if recommendations is None or lookup is None:
        print("Error loading model")
    else:
        print("Recommender model loaded")


init()
