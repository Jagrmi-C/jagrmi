import configparser
import os
import psycopg2
import aiopg

import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

def database_url():
    config = configparser.ConfigParser()
    config.read('config/test.jagrmi.config')
    PORT = config['JagrmiDB']['port']
    HOST = config['JagrmiDB']['host']
    DB = config['JagrmiDB']['database']
    USER = config['JagrmiDB']['user']
    PASSWORD = config['JagrmiDB']['password']
    return f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

def create_conn(db_url):
    conn = psycopg2.connect(db_url, sslmode='require')
    return conn


# __all__ = ['question', 'choice']

meta = MetaData()

test = Table(
    'test', meta,

    # Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('age', Integer, nullable=False)    
)

# question = Table(
#     'question', meta,

#     Column('id', Integer, primary_key=True),
#     Column('question_text', String(200), nullable=False),
#     Column('pub_date', Date, nullable=False)
# )

# choice = Table(
#     'choice', meta,

#     Column('id', Integer, primary_key=True),
#     Column('choice_text', String(200), nullable=False),
#     Column('votes', Integer, server_default="0", nullable=False),

#     Column('question_id',
#            Integer,
#            ForeignKey('question.id', ondelete='CASCADE'))
# )


async def init_pg(app):
    config = configparser.ConfigParser()
    config.read('config/test.jagrmi.config')
    conf = config['JagrmiDB']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        # minsize=conf['min_size'],
        # maxsize=conf['max_size'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
