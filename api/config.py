import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, 'prod_movies.db')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, 'dev_movies.db')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, 'test_movies.db')
    TESTING = True


configurations = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}
