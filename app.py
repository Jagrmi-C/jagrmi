from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")


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
async def variable_handler(request):
    return web.Response(
        text="Hello, {}".format(request.match_info['name']))


app = web.Application()
app.add_routes(routes)
web.run_app(app)
