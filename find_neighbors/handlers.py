from aiohttp import web


async def show(request):
    return web.Response(text='12345')
