from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# from flask_app.models import show


class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    db = 'impression_schema'


    # Validation #################################################
    @staticmethod
    def validate_user(data):

        is_valid = True

        # checks to see if email is valid based on regular expression
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False


        # checks to see if email already exists in database
        email_input = { "email" : data["email"] }
        user_in_db = User.get_by_email(email_input)
        
        if len(user_in_db) != 0:
            flash("Email already exists")
            is_valid = False
            

        # checks to see if username already exists in database
        username_input = { "username" : data["username"] }
        username_in_db = User.get_by_username(username_input)
        
        if len(username_in_db) != 0:
            flash("Username already exists")
            is_valid = False
            

        # checks to see if email was submitted
        if len(data['email']) < 1:
            flash("Please add a valid email")
            is_valid = False
            

        # checks to see if username was submitted
        if len(data['username']) < 1:
            flash("Please add a valid username")
            is_valid = False
            

        # checks to see if password is submitted
        if len(data['password']) < 1:
            flash("Please add a valid password")
            is_valid = False

        
        # checks to see if password confirmation mathces
        if data['password'] != data['confirm_password']:
            flash("Passwords must match exactly")
            is_valid = False

        return is_valid
    
    # ###############################################################


    # Method to add user to database
    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        results  = connectToMySQL('impression_schema').query_db(query, data)
        return results



    # Method to pull a user based on an email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('impression_schema').query_db(query, data)
        
        users = []

        for item in results:
            users.append(User(item))
        return users
    
    
    # Method to pull a user based on a username
    @classmethod
    def get_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL('impression_schema').query_db(query, data)
        
        users = []

        for item in results:
            users.append(User(item))
        return users