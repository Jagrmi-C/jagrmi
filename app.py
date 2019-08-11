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


@routes.get('/500')
async def err_500(request):
    return web.HTTPInternalServerError()


@routes.get('/501')
async def err_501(request):
    return web.HTTPNotImplemented()


@routes.get('/502')
async def err_502(request):
    return web.HTTPBadGateway()


@routes.get('/503')
async def err_503(request):
    return web.HTTPServiceUnavailable()


@routes.get('/504')
async def err_504(request):
    return web.HTTPGatewayTimeout()


@routes.get('/{name}')
async def variable_handler(request):
    return web.Response(
        text="Hello, {}".format(request.match_info['name']))


app = web.Application()
app.add_routes(routes)
web.run_app(app)
