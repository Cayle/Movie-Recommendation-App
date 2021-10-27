import numpy as np
import pandas as pd
import re
from utils import feature_to_binary

import nltk
#from nltk.corpus import stopwords
# from nltk.corpus import stopwords
# stop_words = set(stopwords.words('english'))
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize

data = pd.read_csv('netflix_titles.csv')
print(data['type'])
print(data.groupby('type').count())
data = data.dropna(subset=['cast', 'country', 'rating'])



# def randomize():
#     for i, row in data.iterrows():
        

"""
Developing the recommendation engine using cast, director, country
rating, and genres.
"""

## generating the datsets for the movies. 
movies = data[data['type'] == 'Movie'].reset_index()
movies = movies.drop(['index', 'show_id', 'type', 'date_added', 'release_year', 'duration', 'description'], axis=1)

## generating the datasets for the TV shows.
tv = data[data['type'] == 'TV Show'].reset_index()
tv = tv.drop(['index', 'show_id', 'type', 'date_added', 'release_year', 'duration', 'description'], axis=1)


binary_actors = feature_to_binary("cast", movies)
binary_directors = feature_to_binary("director", movies)
binary_countries = feature_to_binary("country", movies)
binary_genres = feature_to_binary("listed_in", movies)
binary_ratings = feature_to_binary("rating", movies)

binary_movies = pd.concat([binary_actors, binary_directors, binary_countries, binary_genres], axis=1, ignore_index= True)


binary_actors_tv = feature_to_binary("cast", tv)
binary_countries_tv = feature_to_binary("country", tv)
binary_genres_tv = feature_to_binary("listed_in", tv)
binary_ratings_tv = feature_to_binary("rating", tv)


binary_tv = pd.concat([binary_actors_tv, binary_countries_tv, binary_genres_tv], axis=1, ignore_index=True)


def recommender(search):
    cs_list = []
    binary_list = []
    if search in movies['title'].values:
        idx = movies[movies['title'] == search].index.item()
        for i in binary_movies.iloc[idx]:
            binary_list.append(i)
        point1 = np.array(binary_list).reshape(1, -1)
        point1 = [val for sublist in point1 for val in sublist]    
        for j in range(len(movies)):
            binary_list2 = []
            for k in binary_movies.iloc[j]:
                binary_list2.append(k)
            point2 = np.array(binary_list2).reshape(1, -1)
            point2 = [val for sublist in point2 for val in sublist]
            dot_product = np.dot(point1, point2)
            norm_1 = np.linalg.norm(point1)
            norm_2 = np.linalg.norm(point2)
            cos_sim = dot_product / (norm_1 * norm_2)
            cs_list.append(cos_sim)
        movies_copy = movies.copy()
        movies_copy['cos_sim'] = cs_list
        results = movies_copy.sort_values('cos_sim', ascending=False)
        results = results[results['title'] != search]    
        top_results = results.head(5)
        return(top_results)
    elif search in tv['title'].values:
        idx = tv[tv['title'] == search].index.item()
        for i in binary_tv.iloc[idx]:
            binary_list.append(i)
        point1 = np.array(binary_list).reshape(1, -1)
        point1 = [val for sublist in point1 for val in sublist]
        for j in range(len(tv)):
            binary_list2 = []
            for k in binary_tv.iloc[j]:
                binary_list2.append(k)
            point2 = np.array(binary_list2).reshape(1, -1)
            point2 = [val for sublist in point2 for val in sublist]
            dot_product = np.dot(point1, point2)
            norm_1 = np.linalg.norm(point1)
            norm_2 = np.linalg.norm(point2)
            cos_sim = dot_product / (norm_1 * norm_2)
            cs_list.append(cos_sim)
        tv_copy = tv.copy()
        tv_copy['cos_sim'] = cs_list
        results = tv_copy.sort_values('cos_sim', ascending=False)
        results = results[results['title'] != search]    
        top_results = results.head(5)
        return(top_results)
    else:
        return("Title not in dataset. Please check spelling.")




if __name__ == "__main__":
	print(binary_actors[:10])
	print(binary_movies[:10])
	print(binary_actors_tv[:10])
	print(binary_tv[:10])
	x = recommender('The Conjuring')
	for i, row in x.iterrows():
		print(row['title'])
	



