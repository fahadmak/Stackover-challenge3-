import psycopg2
from pprint import pprint

class DatabaseConnection:
    def __init__(self):
        try:
            self.connect = psycopg2.connect(
                "dbname='stack' user='postgres' host='localhost' password='maka1997' port='5432'")
            self.connect.autocommit = True
            self.cursor = self.connect.cursor()
        except:
            pprint("Cannot connect to database")

if __name__== '__main__':
    database_connection = DatabaseConnection()