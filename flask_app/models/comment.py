from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user
from flask_app.models import post



class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_id = data['post_id']


    @classmethod
    def addComment(cls, data):
        query = "INSERT INTO comments (user_id, post_id, content, created_at, updated_at) VALUES (%(user_id)s, %(post_id)s, %(content)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('social_media_schema').query_db(query,data)

    @classmethod
    def get_post_comments(cls, data):
        query = "SELECT * FROM comments WHERE comments.post_id = %(post_id)s;"
        results = connectToMySQL('social_media_schema').query_db(query, data)
        
        return results

    @classmethod
    def edit_post(cls, data):
        query = "UPDATE comments SET caption = %(caption)s, updated_at = NOW() WHERE id = %(id)s"
        results = connectToMySQL('social_media_schema').query_db(query,data)
        return results

    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s"
        results = connectToMySQL('social_media_schema').query_db(query,data)
        return results

