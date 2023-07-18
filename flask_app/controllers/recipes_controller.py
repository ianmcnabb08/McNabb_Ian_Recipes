from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User 
from flask_app.models.recipe import Recipe


@app.route('/recipes')
def recipes_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({"id": session['user_id']})
    recipes = Recipe.get_all()
    if not user:
        return redirect('/logout')
    return render_template('recipes.html', user = user, recipes = recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('create_recipe.html')

@app.route('/recipes/create', methods = ['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipes(request.form):
        return redirect('/recipes/new')
    
    data = {
        "user_id": session['user_id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "created_date": request.form['created_date'],
        "under_30": request.form['under_30'],
        "users_id": session['user_id']
    }
    Recipe.create_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/view/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_recipe_by_id({'id': id})
    return render_template("recipe_view.html", recipe=recipe)

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_recipe_by_id({'id': id})
    return render_template('recipe_edit.html', recipe = recipe)

@app.route('/recipes/edit/go/<int:id>', methods = ['POST'])
def go_edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "created_date": request.form['created_date'],
        "under_30": request.form['under_30'],
        "user_id": session['user_id']
    }
    Recipe.update(data)

    if not Recipe.validate_recipes(request.form):
        return redirect(f'/recipes/edit/{id}')
    return redirect('/recipes')

@app.route('/recipes/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.delete({'id': id})
    return redirect('/recipes')