from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_date = data['created_date']
        self.under_30 = data['under_30']
        self.users_id = data['users_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id;"
        recipes_from_db = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for row in recipes_from_db:
            this_recipe = cls(row)
            users_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": None,
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            this_recipe.creator = user.User(users_data)
            recipes.append(this_recipe)
        return recipes

    @classmethod
    def create_recipe(cls, data):
        query = """
                INSERT INTO recipes (name, description, instructions, created_date, under_30, users_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(created_date)s, %(under_30)s, %(users_id)s);
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        print("CREATE RECIPE RESULT HERE ----->", result)
        return (result)

    @classmethod
    def get_recipe_by_id(cls,data):
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.users_id = users.id
                WHERE recipes.id = %(id)s;
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        result = result[0]
        this_recipe = cls(result)
        users_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": None,
                "created_at": result['created_at'],
                "updated_at": result['updated_at']
        }
        this_recipe.creator = user.User(users_data)
        return this_recipe
    
    @classmethod
    def update(cls,form_data):
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, created_date = %(created_date)s, under_30 = %(under_30)s
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query,form_data)
        print("UPDATE RESULTS HERE ---->", results)
        return results
    
    @classmethod
    def delete(cls,data):
        query = """
            DELETE FROM recipes
            WHERE id = %(id)s;
            """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results

    @staticmethod
    def validate_recipes(form_data):
        is_valid = True
        if len(form_data['name']) < 3: 
            flash("Name must be at least 3 characters in length.")
            is_valid = False
            
        if len(form_data['description']) < 3: 
            flash("Description must be at least 3 characters in length.")
            is_valid = False

        if len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters in length.")
            is_valid = False

        if (form_data['created_date']) == "":
            flash("Date Required")
            is_valid = False

        if 'under_30' not in form_data:
            flash("Under 30 Required")
            is_valid = False

        return is_valid