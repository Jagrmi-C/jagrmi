import configparser
import os
import psycopg2
import aiopg

import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)


def create_conn(db_url):
    conn = psycopg2.connect(db_url, sslmode='require')
    return conn


async def init_pg(app, conf):
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
