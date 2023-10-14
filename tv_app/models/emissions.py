from tv_app import app
from flask import request, render_template, redirect, session, flash
from tv_app.models.loregs import User
from datetime import datetime
from tv_app.config.mysqlconnection import connectToMySQL

class Show:
    def __init__(self, data):
        self.show_id = data['show_id']
        self.title = data['title']
        self.network = data['network']
        self.reldate = data['reldate']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.likes = data['likes']
        


    def __repr__(self):
        return self.title
    
    @classmethod
    def validation_show(cls, data):
        is_valid = True
        if len(data['title']) < 1:
            flash('The show needs a title.', 'create')
            is_valid = False
        if len(data['network']) < 3:
            flash('Network must be more than 3 characters', 'create')
            is_valid = False
        if len(data['reldate']) < 8:
            flash('Date must be in xx/xx/xxxx format.', 'create')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be more than 3 characters', 'create')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO jex_schema.show (title, network, reldate, description, user_id, created_at, updated_at)
                    VALUES (%(title)s, %(network)s, %(reldate)s, %(description)s, %(user_id)s, NOW(), NOW());"""

        results = connectToMySQL('jex_schema').query_db(query, data)
        return results
    
    @classmethod
    def liked(cls, data):
        query = """INSERT INTO aime (user_id, show_id)
                    VALUES (%(user_id)s, %(show_id)s);"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results
    
    @classmethod
    def update(cls, data):
        query = """UPDATE jex_schema.show
                    SET title = %(title)s, network = %(network)s, reldate = %(reldate)s, description = %(description)s, updated_at = NOW()
                    WHERE show_id = %(show_id)s;"""
        
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results 
    
    @classmethod
    def ulike(cls, data):
        query = """UPDATE jex_schema.show
                    SET likes = %(likes)s, updated_at = NOW()
                    WHERE show_id = %(show_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results

    @classmethod
    def get_one(cls, show_id):
        query = """SELECT * FROM jex_schema.show WHERE show_id = %(show_id)s"""
        data = {'show_id': show_id}
        results = connectToMySQL('jex_schema').query_db(query, data)
        fav = cls(results[0])
        return fav
    
    @classmethod
    def get_mine(cls, data):
        query = """SELECT * FROM jex_schema.show WHERE user_id = %(user_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        mshows = []
        if not results:
            return mshows
        else:
            for x in results:
                mshows.append(cls(x))
        return mshows
    
    @classmethod
    def get_others(cls, data):
        query = """SELECT * FROM jex_schema.show WHERE user_id != %(user_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        oshows = []
        if not results:
            return oshows
        else:
            for x in results:
                oshows.append(cls(x))
        return oshows


    @classmethod
    def get_all(cls):
        query = """SELECT * FROM jex_schema.show;"""
        results = connectToMySQL('jex_schema').query_db(query)
        favs = []
        for x in results:
            favs.append(cls(x))
        return favs

    @classmethod
    def allinfo(cls, data):
        query = """SELECT * FROM jex_schema.show
                    JOIN user ON user.user_id = jex_schema.show.user_id
                    WHERE show_id = %(show_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        usershow = results[0]
        print(usershow)
        return usershow
        
    
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM jex_schema.show WHERE show_id = %(show_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results

    
