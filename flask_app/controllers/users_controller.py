from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST']) 
def new_user():
    if not User.validate_user(request.form):
        return redirect('/')
    
    user_id = User.save(request.form)

    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/recipes')


@app.route('/login', methods = ['GET','POST'])
def login():

    if not User.validate_login(request.form):
        return redirect('/')
        
    user_in_db = User.find_user_by_email(request.form)

    if not user_in_db:
        flash("Invalid Email or Password")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email or Password")
        print("USER'S PASSWORD", user_in_db.password)
        print("FORM PASSWORD ------>", request.form['password'])
        return redirect('/')
        
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect("/recipes")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
