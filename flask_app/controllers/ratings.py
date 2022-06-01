from flask_app import app



from flask import render_template, session, redirect, request, flash
from flask_app.models.rating import Rating
from flask_app.models.show import Show
import json
import requests
import os




# Route to process new show rating
@app.route('/process/rating', methods=["POST"])
def process_rating():
    
    api_input = { "media_api_id" : session['show_api_id'] }
    media_in_db = Show.display_show(api_input)
    
    # differentiation btwn mvoie and show
    show_type = 0
    movie_type = 0
    if session['show_type'] == "TVSeries":
        show_type = 1
    else:
        movie_type = 1
    
    # finding average of user ratings
    rating_total = (int(float(request.form['story'])) + int(float(request.form['characters'])) + int(float(request.form['visual_appeal'])) + int(float(request.form['enjoyment'])) + int(float(request.form['music'])) + int(float(request.form['setting']))) / 6
        
    
    # if show / movie is already in db, processing the rating
    if len(media_in_db) != 0:
        media = media_in_db[0]
        data2 ={
        'rating_total' : rating_total,
        'tier' : request.form['tier'],
        'story' : request.form['story'],
        'characters' : request.form['characters'],
        'visual_appeal' : request.form['visual_appeal'],
        'enjoyment' : request.form['enjoyment'],
        'music' : request.form['music'],
        'setting' : request.form['setting'],
        'user_id' : session['user_id'],
        'media_id' : media.id,
        }
        
        rating = Rating.add_rating(data2)
        
        return redirect(f'/process/choice/{session["show_api_id"]}')
    
    
    # if show isn't in the db, adding it, and then processing the rating
    data = {
        'media_api_id' : session['show_api_id'],
        'media_title' : session['show_title'],
        'media_image' : session['show_image'],
        'is_movie' : movie_type,
        'is_show' : show_type
    }
    
    media_id = Show.add_media(data)
    
    data2 ={
        'rating_total' : rating_total,
        'tier' : request.form['tier'],
        'story' : request.form['story'],
        'characters' : request.form['characters'],
        'visual_appeal' : request.form['visual_appeal'],
        'enjoyment' : request.form['enjoyment'],
        'music' : request.form['music'],
        'setting' : request.form['setting'],
        'user_id' : session['user_id'],
        'media_id' : media_id,
    }
    
    rating = Rating.add_rating(data2)
    
    return redirect(f'/process/choice/{session["show_api_id"]}')


# route to process rating update
@app.route('/process/rating/update', methods=["POST"])
def update_rating():
    
    # finding average of user ratings
    rating_total = (int(float(request.form['story'])) + int(float(request.form['characters'])) + int(float(request.form['visual_appeal'])) + int(float(request.form['enjoyment'])) + int(float(request.form['music'])) + int(float(request.form['setting']))) / 6
    
    data = {
        'id': session['rating_id'],
        'rating_total' : rating_total,
        'tier' : request.form['tier'],
        'story' : request.form['story'],
        'characters' : request.form['characters'],
        'visual_appeal' : request.form['visual_appeal'],
        'enjoyment' : request.form['enjoyment'],
        'music' : request.form['music'],
        'setting' : request.form['setting'],
    }
    
    Rating.update_rating(data)
    
    return redirect(f'/process/choice/{session["show_api_id"]}')