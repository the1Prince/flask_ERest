import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRETE_KEY') or '1234'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/rest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False