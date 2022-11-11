from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment


@app.route("/createcomment/<int:post_id>", methods=['POST'])
def createComment(post_id):
    data={
        'content' : request.form['comment'],
        'user_id' : session['user_id'],
        'post_id' : post_id
    }
    Comment.addComment(data)
    data={
        'id' : session['user_id']
    }
    
    return redirect("/dashboard")
    

@app.route("/createcommentexplore/<int:post_id>", methods=['POST'])
def createCommentexplore(post_id):
    data={
        'content' : request.form['comment'],
        'user_id' : session['user_id'],
        'post_id' : post_id
    }
    Comment.addComment(data)
    data={
        'id' : session['user_id']
    }
    
    return redirect("/explore")
