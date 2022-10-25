import numpy as np


def inputRanking(userID, age_binned, user_gender, user_occupation, candidates, i):
    
    input = {    
            "user_id":              np.array([userID]),
            'user_age_binned':      np.array([age_binned]),
            'user_gender':          np.array([user_gender]),
            "user_occupation":      np.array([user_occupation]), 
            "movie_title" :         np.array([candidates['movieID'].iloc[i]]),
            "movie_language" :      np.array([candidates['original_language'].iloc[i]]),
            "movie_length_binned":  np.array([candidates['length_binned'].iloc[i]]),
            "movie_year_binned":    np.array([candidates['year_binned'].iloc[i]]),
            "comedy" :              np.array([candidates['Comedy'].iloc[i]]),
            "mystery":              np.array([candidates['Mystery'].iloc[i]]),            
            "crime":                np.array([candidates['Crime'].iloc[i]]),              
            "drama":                np.array([candidates['Drama'].iloc[i]]),              
            "romance":              np.array([candidates['Romance'].iloc[i]]),            
            "documentary":          np.array([candidates['Documentary'].iloc[i]]),        
            "thriller":             np.array([candidates['Thriller'].iloc[i]]),           
            "action":               np.array([candidates['Action'].iloc[i]]),             
            "animation":            np.array([candidates['Animation'].iloc[i]]),          
            "science_fiction":      np.array([candidates['Science Fiction'].iloc[i]]),    
            "adventure":            np.array([candidates['Adventure'].iloc[i]]),          
            "war":                  np.array([candidates['War'].iloc[i]]),               
            "horror":               np.array([candidates['Horror'].iloc[i]]),             
            "western":              np.array([candidates['Western'].iloc[i]]),            
            "fantasy":              np.array([candidates['Fantasy'].iloc[i]]),            
            "family":               np.array([candidates['Family'].iloc[i]]),             
            "history":              np.array([candidates['History'].iloc[i]]),            
            "tv_movie":             np.array([candidates['TV Movie'].iloc[i]]),           
            "music":                np.array([candidates['Music'].iloc[i]]),              
            "foreign":              np.array([candidates['Foreign'].iloc[i]])
            }
    
    return input