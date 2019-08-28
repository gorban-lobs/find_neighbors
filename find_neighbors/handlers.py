from aiohttp import web


async def show(request):
    return web.Response(text='12345')


async def get_neighbors(request):
    params = request.rel_url.query
    return web.Response(text=str(params['name']))
