import argparse
import asyncio
import asyncpg
import configparser
import os

import aiohttp_jinja2
import jinja2

from aiohttp import web

from family import db
from family.db import init_pg, close_pg
from family.views import routes

from family.db import database_url

async def init_app(is_test=False):
   """Initialize  the application server."""
   app = web.Application()()

   config = configparser.ConfigParser()
   config.read('config/test.jagrmi.config')
   if not is_test:
      conf = config['JagrmiDB']
   else:
      conf = config['JagrmiDBTest']
   dsn = database_url(conf)
   app["conf"] = conf
   import ssl
   ssl_object = ssl.create_default_context(
      capath=r"sertificates/rds-combined-ca-bundle.pem")
   ssl_object.check_hostname = False
   ssl_object.verify_mode = ssl.CERT_NONE
   app["pool"] = await asyncpg.create_pool(dsn=dsn, ssl=ssl_object)

   aiohttp_jinja2.setup(
      app,
      loader=jinja2.FileSystemLoader('tmpl'),
   )
   app.add_routes(routes)
   return app

# app = web.Application()
# aiohttp_jinja2.setup(
#    app,
#    loader=jinja2.FileSystemLoader('tmpl'),
# )
# app.add_routes(routes)
# app.on_startup.append(init_pg)

# app.on_cleanup.append(close_pg)
# web.run_app(app, port=os.getenv('PORT'))

# loop = asyncio.get_event_loop()
# app = loop.run_until_complete(init_app())
# web.run_app(app, port=os.getenv('PORT'))

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-H', '--host', default='0.0.0.0')
   parser.add_argument('-P', '--port', type=int, default=os.getenv('PORT'))
   parser.add_argument("--test", type=bool, default=False)
   args = parser.parse_args()

   loop = asyncio.get_event_loop()
   app = loop.run_until_complete(init_app(args.test))
   web.run_app(app, host=args.host, port=args.port)
