from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import post
from flask_app.models import comment
import re
import base64
import requests
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('^[a-zA-Z]+$')
ALLOWED_EXTENSIONS = { 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' }

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.biography = data['biography']
        self.profile_pic = data['profile_pic']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comment_list=[]
        self.like_list = []
        

    @classmethod
    def addUser(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password, biography, profile_pic, created_at, updated_at ) VALUES ( %(first_name)s,  %(last_name)s,  %(email)s,  %(password)s, %(biography)s, %(profile_pic)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('social_media_schema').query_db(query,data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('social_media_schema').query_db(query, data)
        user = cls(results[0])
        return user

    @classmethod
    def get_user_with_posts(cls, data):
        query = "SELECT * FROM users LEFT JOIN posts ON posts.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('social_media_schema').query_db( query , data )
        user = cls( results[0] )
        postList =[]
        for row in results:
            if row['posts.id']:
                data={
                    'post_id' : row['posts.id']
                }
                commentList = comment.Comment.get_post_comments(data)
                post_data = {
                    "id" : row["posts.id"],
                    "post_pic" : row["post_pic"],
                    "caption" : row["caption"],
                    "user_id" : row["user_id"],
                    "created_at" : row['created_at'],
                    "updated_at" : row['updated_at']
                }
                userpost = post.Post(post_data)
                userpost.comment_list = commentList
                postList.append(userpost)
                user.post_list = postList
                print(user.post_list)
        return user


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('social_media_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def edit_profile(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, biography = %(biography)s, profile_pic = %(profile_pic)s, updated_at = NOW() WHERE id = %(id)s"
        results = connectToMySQL('social_media_schema').query_db(query,data)
        print(results)
        return results

    @staticmethod
    def validate_user(form):
        is_valid = True
        data = {'email' : form['email']}
        email_in_db = User.get_by_email(data)
        if len(form['first_name']) < 2:
            flash("Frist name must be at least 2 letters!")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be at least 2 letters!")
            is_valid = False
        if not NAME_REGEX.match(form['first_name']):
            flash("Name must only consist of letters")
            is_valid = False
        if not NAME_REGEX.match(form['last_name']):
            flash("Name must only consist of letters")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address!")
            is_valid = False
        if email_in_db:
            flash("Email already in use")
            is_valid = False
        if form['password'] != form['confirm password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid


    @staticmethod
    def validate_edit(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash("Frist name must be at least 2 letters!")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be at least 2 letters!")
            is_valid = False
        if not NAME_REGEX.match(form['first_name']):
            flash("Name must only consist of letters")
            is_valid = False
        if not NAME_REGEX.match(form['last_name']):
            flash("Name must only consist of letters")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid


    
    @staticmethod
    def get_pic_url(pic):
        key = 'e2cdf0a47902483877ad3a5b62731ab8'
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": key,
            "image": base64.b64encode(pic.read())
        }
        res = requests.post(url, payload)
        pic_details = res.json()
        profile_pic = pic_details['data']['url'] 
        print(profile_pic)
        return profile_pic
        

        

