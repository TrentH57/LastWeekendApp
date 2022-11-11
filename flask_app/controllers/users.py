from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def entrance():
    return render_template("login.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/register", methods =['POST'])
def register():
    if not request.files['profile_pic']:
        flash('No file selected')
        return redirect('/registration')
    else: 
        pic_file = request.files['profile_pic']
        profile_pic = User.get_pic_url(pic_file)

    if not User.validate_user(request.form):
        return redirect("/")
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
        'biography' : request.form['biography'],
        'profile_pic' : profile_pic
    }

    user_id = User.addUser(data)
    session['user_id'] = user_id
    data = {
        'id' : user_id
    }
    return redirect("/dashboard")

@app.route("/editprofile")
def editprofile():
    if not session:
        flash("Register or Login to edit profile")
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user= User.get_one(data)
    return render_template("editprofile.html", user = user)

@app.route("/processeditprofile", methods =['POST'])
def processeditprofile():
    if not request.files['profile_pic']:
        data={
            'id' : session['user_id']
        }
        user = User.get_one(data)
        if not User.validate_edit(request.form):
            return redirect("/editprofile")
        data = {
        'id' : session['user_id'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : user.password,
        'biography' : request.form['biography'],
        'profile_pic' : user.profile_pic
        }
        User.edit_profile(data)
    else: 
        pic_file = request.files['profile_pic']
        profile_pic = User.get_pic_url(pic_file)
        data={
            'id' : session['user_id']
        }
        user = User.get_one(data)

        if not User.validate_edit(request.form):
            return redirect("/editprofile")
        data = {
            'id' : session['user_id'],
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : user.password,
            'biography' : request.form['biography'],
            'profile_pic' : profile_pic
        }
        User.edit_profile(data)
    
    return redirect("/dashboard")


@app.route("/login", methods=['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect("/dashboard")

@app.route("/dashboard")
def userPage():
    if not session:
        flash("Login to view dashboard")
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_user_with_posts(data)

    return render_template("/dashboard.html", user = user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/explore")
def explore():
    if not session:
        flash("Login to view explore page")
        return redirect('/')
    data={
        'id' : session['user_id']
    }
    user = User.get_one(data)
    allposts = Post.get_all_posts_with_comments()
    return render_template("explore.html", allposts = allposts, user = user)