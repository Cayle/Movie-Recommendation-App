from flask import Flask, jsonify
#from model import recommender, data
from flask_cors import CORS
import numpy as np
import pandas as pd
from api_key import API_KEY
import requests, json

app = Flask(__name__)
CORS(app)


IMAGE_PREFIX = "https://www.themoviedb.org/t/p/w220_and_h330_face"



def get_api_string_title(title):
	API_STRING = f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&language=en-US&query={title}&page=1&include_adult=false"
	return API_STRING

def get_api_string_video(movie_id):
	API_STRING = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US"
	return API_STRING

def get_movie_url(movie_response):
	results = movie_response.get("results", [])
	result = results[0] if len(results) > 0 else {}
	movie_url = "";
	site = result.get("site", "")
	if site == "YouTube":
		movie_url = f"https://www.youtube.com/watch?v={result['key']}"
	elif site == "Vimeo":
		movie_url = f"https://vimeo.com/{result['key']}"
	return movie_url


"""
The below are just sample requests.
"""
@app.before_request
def before():
	print("This is executed before each request.")

@app.route('/<string:name>', methods=['GET'])
def welcome(name):
	return f"Hello {name}"

@app.route('/new', methods=['GET'])
def new():
	d = {'name': 'Caleb', 'age': 5}
	response = jsonify(d)
	return response

@app.route('/status', methods=['GET'])
def status():
	return "Check status" , 218

"""
The above are just sample requests.
"""
@app.route('/movie/<string:term>', methods=['GET'])
def get_movie_details(term):
	api_string = get_api_string_title(term)	
	response = requests.get(api_string)
	print(response.status_code)
	response = response.json()

	show_response = response['results'][0] if len(response['results']) > 0 else {}

	movie_id = show_response.get("id", 550)
	movie_video_response = requests.get(get_api_string_video(str(movie_id)))
	movie_video_response = movie_video_response.json()
	movie_trailer_url = get_movie_url(movie_video_response)

	description = show_response.get("overview", "")
	poster_path = show_response.get("poster_path", "")
	full_poster_path = IMAGE_PREFIX + poster_path if poster_path != "" else poster_path
	release_date = show_response.get("release_date", "")

	movie_details = {'title': term, 'description': description, 'poster_path': full_poster_path, 'release_date': release_date, 'trailer_url': movie_trailer_url}
	return jsonify(movie_details)

@app.route('/search_movie/<string:search_term>', methods=['GET'])
def retrieve_recommendations(search_term):
	recommendations = []
	search_recommendations = recommender(search_term)
	for i, recommendation in search_recommendations.iterrows():
		title = recommendation['title']
		api_string = get_api_string_title(title)
		response = requests.get(api_string)
		print(response.status_code)
		response = response.json()
		show_response = response['results'][0] if len(response['results']) > 0 else {}
		description = show_response.get("overview", "")
		poster_path = show_response.get("poster_path", "")
		full_poster_path = IMAGE_PREFIX + paster_path if poster_path != "" else poster_path
		release_date =  show_response.get("release_date", "")
		recommendation_dict = {'title': title, 'description': description, 'poster_path': full_poster_path, 'release_date': release_date}
		recommendations.append(recommendation_dict)
	return jsonify(recommendations)


@app.route('/random', methods=['GET'])
def random_movies():
	movies = []
	data = pd.read_csv('netflix_titles.csv')
	count = 0
	for i, movie in data.iterrows():
		movie_dict = movie.to_dict()
		print(movie_dict)
		listed_in = "" if pd.isna(movie_dict.get("listed_in", "")) else movie_dict.get("listed_in", "")
		director = "" if pd.isna(movie_dict.get("director", "")) else movie_dict.get("director", "")
		release_year = "" if pd.isna(movie_dict.get("release_year", "")) else movie_dict.get("release_year", "")
		cast = "" if pd.isna(movie_dict.get("cast", "")) else movie_dict.get("cast", "")

		title = movie_dict.get("title", "")
		api_string = get_api_string_title(title)
		response = requests.get(api_string)
		print(response.status_code)
		response = response.json()

		show_response = response['results'][0] if len(response['results']) > 0 else {}

		movie_id = show_response.get("id", 550)
		movie_video_response = requests.get(get_api_string_video(str(movie_id)))
		movie_video_response = movie_video_response.json()
		movie_trailer_url = get_movie_url(movie_video_response)

		description = show_response.get("overview", "")
		poster_path = show_response.get("poster_path", "")
		full_poster_path = IMAGE_PREFIX + poster_path if poster_path != "" else poster_path
		release_date =  show_response.get("release_date", "")

		mov_dict = {'title': title, 'description': description, 'genre': listed_in, 'release_year': release_year, 'director':  
		director, 'cast': cast, 'trailer_url': movie_trailer_url, 'poster_image': full_poster_path}
		movies.append(mov_dict)
		count += 1
		if count == 4:
			break
	return jsonify(movies)





if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', debug=True)
	except:
		print("Error found")