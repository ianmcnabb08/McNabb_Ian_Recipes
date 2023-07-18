from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.update_at = data['updated_at']
        self.recipes = []

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(cls.DB).query_db(query)
        return result

    @classmethod
    def find_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(result)
        if not result:
                return False
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, form_data):
        data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': bcrypt.generate_password_hash(form_data['password'])
        }
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results
    
    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['first_name']) < 1: 
            flash("First Name must be at least 1 characters.")
            is_valid = False
            
        if len(form_data['last_name']) < 1: 
            flash("Last Name must be at least 1 characters.")
            is_valid = False

        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid Email/Password")
            is_valid = False

        if len(form_data['password']) < 8:
            flash("Password MUST be at least 8 characters in length.")
            is_valid = False

        if form_data['password'] != form_data['confirm_pw']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

