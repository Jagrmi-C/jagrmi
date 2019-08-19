import os
import aiohttp_jinja2
import jinja2

from aiohttp import web

from family import db
from family.db import init_pg, close_pg
from family.views import routes


app = web.Application()
aiohttp_jinja2.setup(
   app,
   loader=jinja2.FileSystemLoader('tmpl'),
)
app.add_routes(routes)
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
web.run_app(app, port=os.getenv('PORT'))
