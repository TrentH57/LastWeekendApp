from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment


@app.route("/createpost")
def createPost():
    if not session:
        flash("Register or Login to create posts")
        return redirect('/')

    return render_template("/createPost.html")
    

@app.route("/processpost", methods=['POST'])
def processPost():
    if not request.files['post_pic']:
        flash('No file selected')
        return redirect('/createpost')
    else: 
        pic_file = request.files['post_pic']
        post_pic = Post.get_post_pic_url(pic_file)
        data = {
            'post_pic' : post_pic,
            'caption' : request.form['caption'],
            'user_id' : session['user_id']
        }
    Post.addPost(data)
    return redirect("/dashboard")


@app.route("/editpost/<int:post_id>")
def editpost(post_id):
    if not session:
        flash("Register or Login to edit posts")
        return redirect('/')
    data = {
        'id' : post_id
    }
    post = Post.get_post(data)
    return render_template("editPost.html", post = post)
    

@app.route("/process_edit_post/<int:post_id>", methods=['POST'])
def processeditpost(post_id):
    data = {
        'id' : post_id,
        'caption' : request.form['caption']
    }
    print(request.form['caption'])
    Post.edit_post(data)
    return redirect("/dashboard")


@app.route("/deletepost/<int:post_id>")
def deletepost(post_id):
    if not session:
        flash("Register or Login to delete posts")
        return redirect('/')
    data = {
        'id' : post_id
    }
    Post.delete_post(data)
    return redirect("/dashboard")

