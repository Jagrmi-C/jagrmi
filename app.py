import argparse
import asyncio
import base64
import configparser
import os
import ssl

import asyncpg

import aiohttp_jinja2
import jinja2

from aiohttp import web
from aiohttp_session import get_session, setup, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import settings

from family import db
from family.db import init_pg, close_pg
from family.views import routes


@web.middleware
async def user_middleware(request, handler):
   session = await get_session(request=request)
   request.user = None
   request.info = None
   req_info = request.match_info.get_info()
   path = req_info.get('path')
   # if not path:  # TODO analize
   #    import ipdb; ipdb.set_trace()

   if req_info.get('formatter') and req_info['formatter'] == "/{tail}":
      path = "notcheck"

   if session.get("display_name"):
      # TODO not work in request inst
      request.id = session["google_id"]
      request.display_name = session["display_name"]
      request.email = session["email"]
   elif path not in ("/oauth/login", "/oauth/complete", "notcheck"):
      return web.HTTPFound(
         request.app.router["oauth:login"].url_for()
         )
   response = await handler(request)
   return response


async def init_app(is_test=False):
   """Initialize  the application server."""
   app = web.Application()

   setup(app=app, storage=EncryptedCookieStorage(
      secret_key=settings.SECRET_KEY
      ))
   
   app.middlewares.append(user_middleware)

   ssl_object = ssl.create_default_context(
      capath=r"sertificates/rds-combined-ca-bundle.pem")
   ssl_object.check_hostname = False
   ssl_object.verify_mode = ssl.CERT_NONE

   app["pool"] = await asyncpg.create_pool(
      dsn=settings.DSN,
      ssl=ssl_object
   )

   aiohttp_jinja2.setup(
      app,
      loader=jinja2.FileSystemLoader('tmpl'),
   )
   app.add_routes(routes)
   # app.router.add_static('/static/', path='/static/', name='static')
   app.config = settings
   return app

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('-H', '--host', default='0.0.0.0')
   parser.add_argument('-P', '--port', type=int, default=os.getenv('PORT'))
   # parser.add_argument("--local", type=bool, default=False)
   args = parser.parse_args()

   loop = asyncio.get_event_loop()
   app = loop.run_until_complete(init_app())
   web.run_app(app, host=args.host, port=args.port)
