from flask_app import app



from flask import render_template, session, redirect, request, flash
import json
import requests
import os

from flask_app.models.rating import Rating



# Route to render main homepage
@app.route('/')
def home():
    if 'show_api_id' in session:
        session.pop('show_api_id')
    if 'data_sesh' in session:
        session.pop('data_sesh')
        
    # if not 'popular_movie_data_sesh' in session:
    if session.get('popular_movie_data_sesh') == None:
        
        # account 1
        # r = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/{os.environ.get('imdb_api_key')}")
        
        # account 2
        r = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/k_eygx6g6h")
        
        j=r.json()
        print(j)
        print('================')
        print('================')
        
        data_list_popular_movies = []
        
        for i in j['items']:
            if int(i['rank']) < 11:
                data = {
                    'api_id': i['id'],
                    'title':i['title'],
                    'image':i['image'],
                    'rank':i['rank'],
                }
                data_list_popular_movies.append(data)
            
        session['popular_movie_data_sesh'] = data_list_popular_movies
        
        # print(data_list_popular_movies)
        
        
    # if not 'popular_show_data_sesh' in session:
    if session.get('popular_show_data_sesh') == None:
        
        # account 1
        # r = requests.get(f"https://imdb-api.com/en/API/MostPopularTVs/{os.environ.get('imdb_api_key')}")
        
        # account 2
        r = requests.get(f"https://imdb-api.com/en/API/MostPopularTVs/k_eygx6g6h")
        
        j=r.json()
        print(j)
        print('================')
        print('================')
        
        data_list_popular_shows = []
        
        for i in j['items']:
            if int(i['rank']) < 11:
                data = {
                    'api_id': i['id'],
                    'title':i['title'],
                    'image':i['image'],
                    'rank':i['rank'],
                }
                data_list_popular_shows.append(data)
            
        session['popular_show_data_sesh'] = data_list_popular_shows
        
        # print(data_list_popular_shows)
    
    
    return render_template("homepage.html")



# Route to process search api call
@app.route('/process/search', methods=["POST"])
def process_search():
    if 'show_api_id' in session:
        session.pop('show_api_id')
        session.pop('show_title')
        session.pop('show_image')
        session.pop('show_plot')
        session.pop('show_full_title')
        session.pop('show_genres')
        session.pop('show_imdb')
        session.pop('show_rating')
        session.pop('show_type')
    
    if not 'data_sesh' in session or session['data_sesh'][0]['search'] != request.form['search']:
        search = request.form['search']
        print(request.form['search'])
        
        # account 1
        # r = requests.get(f"https://imdb-api.com/en/API/SearchTitle/{os.environ.get('imdb_api_key')}/{search}")
        
        # account 2
        r = requests.get(f"https://imdb-api.com/en/API/SearchTitle/k_eygx6g6h/{search}")
        
        j=r.json()
        # print(j)
        
        # print(j['results'])
        
        data_list = []
        
        for i in j['results']:
            data = {
                'search': search,
                'api_id': i['id'],
                'title':i['title'],
                'image':i['image']
            }
            data_list.append(data)
            
        session['data_sesh'] = data_list
        
        # print(data_list)
    
    return render_template("show_searches.html")


# Route to process search choice
@app.route('/process/choice/<api_id>')
def process_search_choice(api_id):
    if not 'show_api_id' in session:
        
        # account1
        # r = requests.get(f"https://imdb-api.com/en/API/Title/{os.environ.get('imdb_api_key')}/{api_id}")
        
        # account2
        r = requests.get(f"https://imdb-api.com/en/API/Title/k_eygx6g6h/{api_id}")
        
        j=r.json()
        print(j)
        print('================')
        print('================')
        
        session['show_api_id'] = j['id']
        session['show_title'] = j['title']
        session['show_image'] = j['image']
        session['show_plot'] = j['plot']
        session['show_full_title'] = j['fullTitle']
        session['show_genres'] = j['genres']
        session['show_imdb'] = j['imDbRating']
        session['show_rating'] = j['contentRating']
        session['show_type'] = j['type']
        
        user_rating = 1
        
    if 'user_id' in session:
        data = {
            'media_api_id': session['show_api_id'],
            'user_id': session['user_id']
        }
        
        user_rating = Rating.show_user_rating(data)
        if user_rating != 1:
            session['rating_id'] = user_rating.id
        return render_template("show_search_choice.html", user_rating = user_rating)
        
        session['show_api_id'] = j['id']
        session['show_title'] = j['title']
        session['show_image'] = j['image']
        session['show_plot'] = j['plot']
        session['show_full_title'] = j['fullTitle']
        session['show_genres'] = j['genres']
        session['show_imdb'] = j['imDbRating']
        session['show_rating'] = j['contentRating']
        session['show_type'] = j['type']
    
    
    return render_template("show_search_choice.html", user_rating = 1)


# route to take user to all shows page
@app.route('/all/shows')
def all_shows():
    if 'show_api_id' in session:
        session.pop('show_api_id')
        session.pop('show_title')
        session.pop('show_image')
        session.pop('show_plot')
        session.pop('show_full_title')
        session.pop('show_genres')
        session.pop('show_imdb')
        session.pop('show_rating')
        session.pop('show_type')
    
    # if not 'popular_show_data_sesh' in session:
    if session.get('all_show_data_sesh') == None:
        
        # account 1
        # r = requests.get(f"https://imdb-api.com/en/API/MostPopularTVs/{os.environ.get('imdb_api_key')}")
        
        # account 2
        r = requests.get(f"https://imdb-api.com/en/API/MostPopularTVs/k_eygx6g6h")
        
        j=r.json()
        print(j)
        print('================')
        print('================')
        
        all_shows = []
        
        for i in j['items']:
                data = {
                    'api_id': i['id'],
                    'title':i['title'],
                    'image':i['image'],
                    'rank':i['rank'],
                }
                all_shows.append(data)
    
    return render_template("all_shows.html", all_shows = all_shows)


# route to take user to all movies page
@app.route('/all/movies')
def all_movies():
    if 'show_api_id' in session:
        session.pop('show_api_id')
        session.pop('show_title')
        session.pop('show_image')
        session.pop('show_plot')
        session.pop('show_full_title')
        session.pop('show_genres')
        session.pop('show_imdb')
        session.pop('show_rating')
        session.pop('show_type')
    
    # if not 'popular_movie_data_sesh' in session:
    if session.get('all_movie_data_sesh') == None:
        
        # account 1
        # r = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/{os.environ.get('imdb_api_key')}")
        
        # account 2
        r = requests.get(f"https://imdb-api.com/en/API/MostPopularMovies/k_eygx6g6h")
        
        j=r.json()
        print(j)
        print('================')
        print('================')
        
        all_movies = []
        
        for i in j['items']:
                data = {
                    'api_id': i['id'],
                    'title':i['title'],
                    'image':i['image'],
                    'rank':i['rank'],
                }
                all_movies.append(data)
            
    
    return render_template("all_movies.html", all_movies = all_movies)