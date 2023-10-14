import re
from flask import flash
from tv_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def __repr__(self):
        return self.first_name

    @staticmethod
    def validation_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 3:
            flash('First name must be greater than 3 characters!', 'register')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name must be greater than 3 characters!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address!', 'register')
            is_valid = False
        query = """SELECT * FROM user WHERE email = %(email)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        if len(results) != 0:
            flash('Email already exists', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be greater than 8 characters!', 'register')
            is_valid = False
        if data['password'] != data['confirm']:
            flash('Password does not match!', 'register')
            is_valid = False   
        return is_valid

    @classmethod
    def save(cls, data):
        query = """INSERT INTO user (first_name, last_name, email, password, created_at, updated_at)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"""
        
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results 
    
    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM user WHERE user_id = %(user_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        profile = cls(results[0])
        return profile
    
    @classmethod
    def get_id(cls, data):
        query = """SELECT * FROM user WHERE email = %(email)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        profile = cls(results[0])
        return profile
        
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM user;"""
        results = connectToMySQL('jex_schema').query_db(query)
        profiles = []
        for person in results:
            profiles.append(cls(person))
        return profiles

    @classmethod                            #running for login validation 
    def get_email(cls, data):
        query = """SELECT * FROM user WHERE email = %(email)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    