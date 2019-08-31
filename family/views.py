import asyncpg
import aiopg
import aiohttp_jinja2

from aiohttp import web

from family import db
from settings import DSN

routes = web.RouteTableDef()


@routes.get("/db")
async def get_names(request):
    connection = await aiopg.connect(DSN)
    async with connection.cursor() as cur:
        await cur.execute("SELECT * FROM person_table")
        res = await cur.fetchall()
        return web.Response(text=str(res))

@routes.get("/testselect")
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
