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
config.read('config/test.jagrmi.config')
conf = config['JagrmiDB']
PORT = conf['port']
HOST = conf['host']
DB = conf['database']
USER = conf['user']
PASSWORD = conf['password']

def database_url(conf):
    return f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

DSN = database_url(conf)

DATABASE = {
    'database': DB,
    'password': HOST,
    'user': USER,
    'host': HOST,
    'port': PORT,
}

try:
    from .settings_local import *  # noqa
except ImportError:
    pass