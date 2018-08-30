from api.database_handler import DatabaseConnection
import os
from api.app import create_app

db = DatabaseConnection()
db.create_tables()
app = create_app('DEVELOPMENT')
if __name__ == '__main__':
    app.run()