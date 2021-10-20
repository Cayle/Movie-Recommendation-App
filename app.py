from flask import Flask, jsonify
from model import recommender
import numpy as np
import pandas as pd
from api_key import API_KEY
import requests, json

app = Flask(__name__)



def get_api_string(title):
	API_STRING = f'https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&language=en-US&query={title}&page=1&include_adult=false'
	return API_STRING

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
	return jsonify(d)

@app.route('/status', methods=['GET'])
def status():
	return "Check status" , 218

"""
The above are just sample requests.
"""

@app.route('/movie/<string:search_term>', methods=['GET'])
def retrieve_recommendations(search_term):
	recommendations = []
	search_recommendations = recommender(search_term)
	for i, recommendation in search_recommendations.iterrows():
		title = recommendation['title']
		api_string = get_api_string(title)
		response = requests.get(api_string)
		print(response.status_code)
		response = response.json()
		show_response = response['results'][0] if len(response['results']) > 0 else {}
		description = show_response.get("overview", "")
		poster_path = show_response.get("poster_path", "")
		release_date =  show_response.get("release_date", "")
		recommendation_dict = {'title': title, 'description': description, 'poster_path': poster_path, 'release_date': release_date}
		recommendations.append(recommendation_dict)
	return jsonify(recommendations)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 105)