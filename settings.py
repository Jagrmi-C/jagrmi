import configparser
# import logging
import os

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

DEBUG = False

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# logger.addHandler(console)

config = configparser.ConfigParser()
config.read("config/test.jagrmi.config")

conf = config["JagrmiDB"]

DATABASE = {
    'database': conf['database'],
    'password': conf['password'],
    'user': conf['user'],
    'host': conf['host'],
    'port': conf['port'],
}

def database_url(conf):
    PORT = conf["port"]
    HOST = conf["host"]
    DB = conf["database"]
    USER = conf["user"]
    PASSWORD = conf["password"]
    return f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

DSN = database_url(conf)

SECRET_KEY='5Vqi6xKb-nBLmFkXjRdz0rWVq7Iv7_hvQdHdasQgTPU='
REDIRECT_URI='http://localhost:8080/oauth/login'
OAUTH_REDIRECT_PATH = '/oauth/login'

GOOGLE_ID = '1037729643312-ka43qhgsf27emk7e32te1ijj3mv2n8k2.apps.googleusercontent.com'
GOOGLE_SECRET = 'A6A3Ge0zk3VqDfiVrrt9pp_y'

TEST_COUNT = 0

# DELETE AFTER
import logging

FH_LEVEL = logging.ERROR
CH_LEVEL = logging.ERROR

try:
    from settings_local import *  # noqa
except ImportError:
    pass
