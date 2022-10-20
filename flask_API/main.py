from flask import Flask
from Models.model import recommendMovies

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/recommend/<userID>', methods = ['GET'])
def getRecommendations(userID):
    movie_list = recommendMovies(userID)
    return ','.join(movie_list)