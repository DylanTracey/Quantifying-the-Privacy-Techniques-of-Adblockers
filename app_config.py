import os


class BassConfig():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database_temp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BassConfig):
    DEBUG = True


class TestConfig(BassConfig):
    TESTING = True


class ProductionConfig(BassConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
