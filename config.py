import os

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DATABASE_URI = 'postgresql://localhost/stackoverflow'

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
class Testing(object):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True

app_config = {
    'DEVELOPMENT' : Development,
    'PRODUCTION': Production,
    'TESTING': Testing
}
