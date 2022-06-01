from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import show


class Rating:
    def __init__(self, data):
        self.id = data['id']
        self.rating_total = data['rating_total']
        self.tier = data['tier']
        self.story = data['story']
        self.characters = data['characters']
        self.visual_appeal = data['visual_appeal']
        self.enjoyment = data['enjoyment']
        self.music = data['music']
        self.setting = data['setting']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.media_id = data['media_id']
        
        self.media = {}



    # method to add a rating to the ratings table
    @classmethod
    def add_rating(cls, data):
        query = "INSERT INTO ratings (rating_total, tier, story, characters, visual_appeal, enjoyment, music, setting, user_id, media_id) VALUES (%(rating_total)s, %(tier)s, %(story)s, %(characters)s, %(visual_appeal)s, %(enjoyment)s, %(music)s, %(setting)s, %(user_id)s, %(media_id)s);"
        results = connectToMySQL('impression_schema').query_db(query, data)
        return results
    
    
    # method to show a user's rating for a single show
    @classmethod
    def show_user_rating(cls, data):
        query = "SELECT * FROM ratings JOIN medias ON ratings.media_id = medias.id WHERE media_api_id = %(media_api_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL('impression_schema').query_db(query, data)
        
        if len(results) != 0:
            rating = cls(results[0])
            media_data = {
                'id': results[0]['id'],
                'media_api_id': results[0]['media_api_id'],
                'media_title': results[0]['media_title'],
                'media_image': results[0]['media_image'],
                'is_movie': results[0]['is_movie'],
                'is_show': results[0]['is_show'],
                'created_at': results[0]['created_at'],
                'updated_at': results[0]['updated_at'],
                }
            rating.media = show.Show(media_data)
            return rating
        results = 1
        return results
    
    
    # method to update a user's rating for a show
    @classmethod
    def update_rating(cls, data):
        query = "UPDATE ratings SET rating_total = %(rating_total)s, tier = %(tier)s, story = %(story)s, characters = %(characters)s, visual_appeal = %(visual_appeal)s, enjoyment = %(enjoyment)s, music = %(music)s, setting = %(setting)s WHERE id = %(id)s"
        results = connectToMySQL('impression_schema').query_db(query, data)