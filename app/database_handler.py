import psycopg2

from .model import User

from werkzeug.security import generate_password_hash

from flask import current_app

class DatabaseConnection:
    def __init__(self):
       
        self.connect = psycopg2.connect(
            "dbname='stackoverflow' user='postgres' host='localhost' password='maka1997' port='5432'")
        self.cursor = self.connect.cursor()

    def create_tables(self):
        """ create tables in the PostgreSQL database"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS questions (
                    qn_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    body TEXT,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS answers (
                    an_id SERIAL PRIMARY KEY,
                    descr TEXT NOT NULL,
                    qn_id INTEGER NOT NULL,
                    FOREIGN KEY (qn_id)
                    REFERENCES questions (qn_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)
        
        for command in commands:
            self.cursor.execute(command)
            self.connect.commit()
        # close communication with the PostgreSQL database server
        # self.cursor.close()
       

    def insert_user(self, name, username, password):
        """ insert a user into the users table """
        command = "INSERT INTO users(name, username, password)\
                    VALUES('{}','{}', '{}');".format(name,
                                             username,
                                             generate_password_hash
                                             (password))
        self.cursor.execute(command)
        self.connect.commit()

    def get_user_by_username(self, username):
        command = "SELECT * FROM users WHERE username = '{}'".format(username)
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        user = User(result[0], result[1], result[2], result[3])
        return user

    

