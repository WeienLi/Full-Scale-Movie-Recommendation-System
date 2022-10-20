from flask import Flask
app = Flask(__name__)

import json
from Models.model import recommendMovies

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/recommend/<userID>', methods = ['GET'])
def getRecommendations(userID):
    move_list = recommendMovies(userID)
    return json.dumps(move_list)