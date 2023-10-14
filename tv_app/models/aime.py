from tv_app import app
from flask import request, render_template, redirect, session, flash
from tv_app.config.mysqlconnection import connectToMySQL

class Aime:
    def __init__(self, data):
        self.aime_id = data['aime_id']
        self.user_id = data['user_id']
        self.show_id = data['show_id']

        
    @classmethod
    def save(cls, data):
        query = """INSERT INTO aime (user_id, show_id)
                    VALUES (%(user_id)s, %(show_id)s);"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results

    @classmethod
    def user_like(cls, data):
        query = """SELECT * FROM aime WHERE user_id = %(user_id)s AND show_id = %(show_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        ulike = []
        if not results:
            count = len(ulike)
            return count
        else: 
            for x in results:
                ulike.append(cls(x))
        count = len(ulike)
        return count
    
    @classmethod
    def get_likes(cls, data):
        query = """SELECT * FROM aime WHERE show_id = %(show_id)s;"""
        results = connectToMySQL("jex_schema").query_db(query, data)
        count = []
        if not results:
            return len(count)
        else:
            for x in results:
                count.append(cls(x))
        return len(count)
    
    @classmethod
    def gal(cls, data):
        query = """SELECT * FROM jex_schema.show
                    JOIN aime ON jex_schema.show.show_id = aime.show_id
                    JOIN user ON user.user_id = aime.user_id
                    WHERE jex_schema.show.show_id = %(show_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        gal = []
        print(results)
        if not results:
            return gal
        for x in results:
            gal.append(x)
        print(gal)
        return gal
        
    
    @classmethod
    def deletelike(cls, data):
        query = """DELETE FROM aime WHERE show_id = %(show_id)s AND user_id = %(user_id)s;"""
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, show_id):
        query = """DELETE FROM aime WHERE show_id = %(show_id)s;"""
        data = {'show_id' : show_id}
        results = connectToMySQL('jex_schema').query_db(query, data)
        return results