from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re



class Show:
    def __init__(self, data):
        self.id = data['id']
        self.media_api_id = data['media_api_id']
        self.media_title = data['media_title']
        self.media_image = data['media_image']
        self.is_movie = data['is_movie']
        self.is_show = data['is_show']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    # method to add a show to the medias table
    @classmethod
    def add_media(cls, data):
        query = "INSERT INTO medias (media_api_id, media_title, media_image, is_movie, is_show) VALUES (%(media_api_id)s, %(media_title)s, %(media_image)s, %(is_movie)s, %(is_show)s);"
        results = connectToMySQL('impression_schema').query_db(query, data)
        return results
    
    
    # method to show a show based on media_api_id
    @classmethod
    def display_show(cls, data):
        query = "SELECT * FROM medias WHERE media_api_id = %(media_api_id)s;"
        results = connectToMySQL('impression_schema').query_db(query, data)
        
        shows = []

        for item in results:
            shows.append(Show(item))
        return shows
