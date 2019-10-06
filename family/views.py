import logging
import os

import asyncpg
import aiopg
import aiohttp_jinja2

from aiohttp import web

from family import db
from settings import DSN, FH_LEVEL, CH_LEVEL
from aioauth_client import GoogleClient
from aiohttp_session import get_session

from family import models

routes = web.RouteTableDef()

f_name = "log/views.log"

logger = logging.getLogger("family.views")
logger.setLevel(logging.DEBUG)
os.makedirs(os.path.dirname(f_name), exist_ok=True)
fh = logging.FileHandler(f_name, mode="a", encoding=None, delay=False)
fh.setLevel(FH_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(CH_LEVEL)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


@routes.get("/db")
async def get_names(request):
    connection = await aiopg.connect(DSN)
    async with connection.cursor() as cur:
        await cur.execute("SELECT * FROM person_table")
        res = await cur.fetchall()
        return web.Response(text=str(res))

@routes.get("/testselect", name='testselect')
async def test_add_user(request):
    # conn = await asyncpg.connect(dsn=DSN)
    conn = request.app["pool"]
    res = await conn.fetch("SELECT * FROM person_table")
    return web.Response(text=str(res))


@routes.get("/testadd")
async def test_add_person(request):
    from family.models import Person
    from datetime import datetime
    # import pdb; pdb.set_trace()
    name = "test2"
    lastname = "tester2"
    birthdate = datetime.now().strftime("%Y-%m-%d")
    birthplace = "test2"
    _sql = """
            INSERT INTO person_table
            (name, lastname, birthdate, birthplace)
            VALUES ('test3', 'test3','2019-02-30' ,'test2'); 
            SELECT * from person_table;
            """
    res = await request.app["pool"].execute(_sql)
    return web.Response(text=f"Hello, world {res}")


# @routes.get("/initdb")
# async def index_db(request):
#     async with request.app['db'].acquire() as conn:
#         cursor = await conn.execute(db.test.select())
#         records = await cursor.fetchall()
#         questions = [dict(q) for q in records]
#         return web.Response(text=str(questions))


@routes.get("/oauth/login", name="oauth:login")
async def oauth_login(request):
    google_client = GoogleClient(
        client_id=request.app.config.GOOGLE_ID,
        client_secret=request.app.config.GOOGLE_SECRET,
    )
    logger.debug("Start OAUTH2")
    if not request.url.query.get("code"):
        logger.debug("Code isn't exist")
        return web.HTTPFound(
            google_client.get_authorize_url(
                redirect_uri=request.app.config.REDIRECT_URI,
                scope="email profile",
            )
        )

    logger.debug("Code {} was received successfully".format(
        request.url.query["code"]
    ))

    token, data = await google_client.get_access_token(
        request.url.query["code"],
        redirect_uri=request.app.config.REDIRECT_URI
    )

    logger.debug("Token {} was received successfully".format(
        token
    ))

    session = await get_session(request)
    session['token'] = token

    logger.debug("Redirect URL: {}".format(
        request.app.config.REDIRECT_URI
    ))

    return web.HTTPFound(request.app.router["oauth:complete"].url_for())


@routes.get("/oauth/complete", name="oauth:complete")
async def oauth_complete(request):
    session = await get_session(request=request)
    if session["token"] is None:
        logger.debug("No token, redirect to login page")
        return web.HTTPFound(request.app.router['oauth:login'].url_for())

    client = GoogleClient(
        client_id=request.app.config.GOOGLE_ID,
        client_secret=request.app.config.GOOGLE_SECRET,
        access_token=session["token"]
    )
    user, info = await client.user_info()
    google_id = info.get("id")
    display_name = info.get("name")
    email = info.get("email")

    logger.debug("Vars:{}, {}, {}.".format(
        google_id, display_name, email
    ))

    async with request.app["pool"].acquire() as conn:
        row = await conn.fetchrow(
            'SELECT * FROM user_google WHERE google_id= $1', google_id
        )
        if not row:
            logger.info(
                "Add a new google account with ID: {}.".format(google_id)
            )
            _sql = f"""
            INSERT INTO user_google
            (google_id, google_user, google_email)
            VALUES ('{google_id}', '{display_name}', '{email}'); 
            """
            res = await request.app["pool"].execute(_sql)
        else:
            logger.info(
                "Update existing account with ID: {}.".format(google_id)
            )
            _sql = f"""
            UPDATE user_google
            SET
            google_user='{display_name}', google_email='{email}'
            WHERE google_id='{google_id}'; 
            """
            res = await request.app["pool"].execute(_sql)
            # import ipdb; ipdb.set_trace()

    session['display_name'] = display_name
    session['google_id'] = google_id
    session['email'] = email
    logger.debug(
        "Add to current session information ({}).".format(display_name)
    )
    return web.HTTPFound(request.app.router['testselect'].url_for())


@routes.get('/')
async def hello(request):
    return web.Response(text=f"Hello, world {DSN}")


@routes.view("/view")
class MyView(web.View):
    async def get(self):
        data = {'some': 'data'}
        return web.json_response(data)

    async def post(self):
        return web.HTTPForbidden()


@routes.view("/500")
class Excption500View(web.View):
    async def get(self):
        return web.HTTPInternalServerError()

    async def post(self):
        return web.HTTPInternalServerError()


@routes.view("/501")
class Excption501View(web.View):
    async def get(self):
        return web.HTTPNotImplemented()

    async def post(self):
        return web.HTTPNotImplemented()


@routes.view("/502")
class Excption502View(web.View):
    async def get(self):
        return web.HTTPBadGateway()

    async def post(self):
        return web.HTTPBadGateway()


@routes.view("/503")
class Excption503View(web.View):
    async def get(self):
        return web.HTTPServiceUnavailable()

    async def post(self):
        return web.HTTPServiceUnavailable()


@routes.view("/504")
class Excption504View(web.View):
    async def get(self):
        return web.HTTPGatewayTimeout()

    async def post(self):
        return web.HTTPGatewayTimeout()


@routes.get('/{name}')
@aiohttp_jinja2.template('index.html')
async def variable_handler(request):
    # return web.Response(
    #     text="Hello, {}".format(request.match_info['name']))
    return {}
