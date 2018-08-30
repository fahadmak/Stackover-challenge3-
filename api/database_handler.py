import os
import psycopg2
import sys
from pprint import pprint
from werkzeug.security import generate_password_hash


class DatabaseConnection:
    def __init__(self):
        if os.getenv('FLASK_ENV') == 'TESTING':
            try:
                self.connect = psycopg2.connect("dbname= 'testdb' user='postgres' "
                                                "host='localhost' password='maka1997' port='5432'")
                self.cursor = self.connect.cursor()
            except psycopg2.OperationalError as e:
                print('Unable to connect!\n{0}').format(e)
                sys.exit(1)           
        else:
            try:
                self.connect = psycopg2.connect("dbname= 'stackoverflow' user='postgres'"
                                                " host='localhost' password='maka1997' port='5432'")
                self.cursor = self.connect.cursor()
            except psycopg2.OperationalError as e:
                print('Unable to connect!\n{0}').format(e)
                sys.exit(1)    

    def create_tables(self):
        """ create tables for the database"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
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

    def insert_user(self, name, username, password):
        """ insert a user into the users table """
        command = "INSERT INTO users(name, username, password)\
                    VALUES('{}','{}', '{}');".format(name, username,
                    generate_password_hash(password))
        pprint(command)
        self.cursor.execute(command)
        self.connect.commit()

    def get_user_by_username(self, username):
        """ select a user by username in the users table """
        command = "SELECT * FROM users WHERE username = '{}'".format(username)
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            user = {
                    "user_id": result[0],
                    "name": result[1],
                    "username": result[2],
                    "password": result[3]
                }
        return user

    def get_all_users(self):
        """ select all users the users table """
        command = "SELECT * FROM users" 
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        print(results)
        users = []
        for result in results:
            user = {
                "user_id": result[0],
                "name": result[1],
                "username": result[2],
                "password": result[3]
            }
            users.append(user)
        return users

    def get_question_by_qnid(self, qn_id):
        """ select a question by question id in the questions table """
        command = "SELECT * FROM questions WHERE qn_id = '{}'".format(qn_id)
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            question = {
                    "qn_id": result[0],
                    "title": result[1],
                    "body": result[2],
                    "user_id": result[3]
                }
            print(question)
            return question

    def insert_answer(self, descr, qn_id, user_id):
        """ insert a answer into the answers table """
        command = "INSERT INTO answers(descr, qn_id, user_id)\
                    VALUES('{}', '{}', '{}');".format(descr, qn_id, user_id)

        pprint(command)
        self.cursor.execute(command)
        self.connect.commit()

    def get_all_questions(self):
        """ select all questions in questions table """
        command = "SELECT * FROM questions" 
        self.cursor.execute(command)
        results = self.cursor.fetchall()
        if results is []:
            return []
        else:
            questions = []
            for result in results:
                question = {
                    "qn_id": result[0],
                    "title": result[1],
                    "body": result[2],
                    "user_id": result[3],
                }
                questions.append(question)
            return questions

    def insert_question(self, title, body, user_id):
        """ insert a question into the questions table """
        command = "INSERT INTO questions(title, body, user_id)\
                    VALUES('{}', '{}', '{}');".format(title, body, user_id)

        pprint(command)
        self.cursor.execute(command)
        self.connect.commit()

    def delete_question_byid(self, qn_id, user_id):
        command = "DELETE FROM questions WHERE qn_id = '{}' AND user_id ='{}'".format(qn_id, user_id)
        self.cursor.execute(command)
        rows_deleted = self.cursor.rowcount
        self.connect.commit()
        return rows_deleted

    def drop_all(self):
        commands = ("DROP TABLE IF EXISTS answers", "DROP TABLE IF EXISTS questions", "DROP TABLE IF EXISTS users;")
        for command in commands:
            self.cursor.execute(command)
            self.connect.commit()