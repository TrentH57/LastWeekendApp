from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user
from flask_app.models import comment
import re
import base64
import requests

ALLOWED_EXTENSIONS = { 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' }


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.post_pic = data['post_pic']
        self.caption = data['caption']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.comment_list=[]
        self.like_list = []


    @classmethod
    def addPost(cls, data):
        query = "INSERT INTO posts ( post_pic, caption, user_id, created_at, updated_at ) VALUES ( %(post_pic)s, %(caption)s, %(user_id)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('social_media_schema').query_db(query,data)

    @classmethod
    def get_post(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL('social_media_schema').query_db(query, data)
        post = cls(results[0])
        return post

    @classmethod
    def get_all_posts_with_comments(cls):
        query = "SELECT * FROM posts LEFT JOIN comments ON comments.post_id = posts.id;"
        results = connectToMySQL('social_media_schema').query_db(query)
        postList = []
        for row in results:
            post = cls(row)
            commentList =[]
            comment_data = {
                "id" : row["comments.id"],
                "content" : row["content"],
                "post_id" : row["post_id"],
                "user_id" : row["user_id"],
                "created_at" : row['comments.created_at'],
                "updated_at" : row['comments.updated_at']
            }
            postComment = comment.Comment(comment_data)
            commentList.append(postComment)
            print(commentList)
            post.comment_list = commentList
            postList.append(post)
        return postList


    @classmethod
    def edit_post(cls, data):
        query = "UPDATE posts SET caption = %(caption)s, updated_at = NOW() WHERE id = %(id)s"
        results = connectToMySQL('social_media_schema').query_db(query,data)
        return results

    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s"
        results = connectToMySQL('social_media_schema').query_db(query,data)
        return results




    @staticmethod
    def get_post_pic_url(pic):
        key = 'e2cdf0a47902483877ad3a5b62731ab8'
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": key,
            "image": base64.b64encode(pic.read())
        }
        res = requests.post(url, payload)
        pic_details = res.json()
        post_pic = pic_details['data']['url']
        return post_pic
        

