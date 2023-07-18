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
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/recipes')


@app.route('/login', methods = ['POST'])
def login():
    user_in_db = User.find_user_by_email(request.form)

    if not user_in_db and not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email")
        print("ITS THE EMAIL")
        return redirect("/")
    
    print(user_in_db.password)
    print(request.form['password'])
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect("/recipes")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
