import json
import os

def recommendMovies(userID):
    # load the cached recommendations JSON
    root = os.path.join(os.path.dirname(__file__))
    with open(os.path.join(root, 'cache', 'recommendations.json'), 'r') as f:
        recommendations = json.load(f)
    
    # Return a pre-defined (random) result if the user ID is not in the recommendations
    if userID not in recommendations:
        userID = 0
    
    rec_list = recommendations[str(userID)]
    # load the cached lookup table JSON
    with open(os.path.join(root, 'cache', 'lookuptable.json'), 'r') as f:
        lookup = json.load(f)
    # return the movie titles
    return [lookup[str(movieID)] for movieID in rec_list]
