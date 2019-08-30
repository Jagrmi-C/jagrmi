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

try:
    from settings_local import *  # noqa
except ImportError:
    pass
