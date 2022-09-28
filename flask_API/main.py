from flask import Flask
app = Flask(__name__)

import json

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/recommend/<userID>', methods = ['GET'])
def getRecommendations(userID):
    move_list = []
    for i in range(10):
        movieNmae = "movie " + str(i)
        move_list.append(movieNmae)
    return json.dumps(move_list)