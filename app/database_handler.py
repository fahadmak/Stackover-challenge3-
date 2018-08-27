import psycopg2
from flask import current_app

class DatabaseConnection:
    def __init__(self):
        if current_app.config["TESTING"]:
            self.connect = psycopg2.connect(
                "dbname='test_db' user='postgres' host='localhost' password='maka1997' port='5432'")
            self.connect.autocommit = True
            self.cursor = self.connect.cursor()
        else:
            self.connect = psycopg2.connect(
                "dbname='stackover' user='postgres' host='localhost' password='maka1997' port='5432'")
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
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS answers (
                    an_id SERIAL PRIMARY KEY,
                    descr TEXT NOT NULL,
                    FOREIGN KEY (qn_id)
                        REFERENCES questions (qn_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
                    FOREIGN KEY (user_id)
                        REFERENCES users (user_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)
        try:
            for command in commands:
                self.cursor.execute(command)
            # close communication with the PostgreSQL database server
            self.cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.connect is not None:
                self.connect.close()

    def insert_user(self, name, username, password):
        """ insert a user into the users table """
        command = """INSERT INTO users(name, username, password)
                    VALUES(name, username, password);"""
        self.cursor.execute(command)
        self.connect.commit()
