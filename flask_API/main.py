from flask import Flask
from Models.model import recommendMovies
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info("app_info", "Monitoring flask API", version="1.0.0")

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/recommend/<userID>', methods = ['GET'])
def getRecommendations(userID):
    movie_list = recommendMovies(userID)
    return ', '.join(movie_list)