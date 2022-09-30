# Import the model here
from pyspark.ml.recommendation import ALSModel

def recommendMovies(userID):
    ''' This function takes in a user ID and returns a list of 20 recommended movies for that user.'''
    
    # Load the model
    model = ALSModel.load("/ALS/metadata/_SUCCESS")
    # Get the recommendations
    recommendations = model.recommendForAllUsers(10)
    # Get the recommendations for the user
    user_recommendations = recommendations.filter(recommendations.userId == userID)
    # Get the movie names
    movie_names = user_recommendations.select("recommendations.movieIndex").collect()
    # Return the movie names
    return movie_names