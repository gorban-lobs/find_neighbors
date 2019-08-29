from aiohttp import web

from db_logic import add_user_to_db, get_neighbors_from_db


async def show(request):
    return web.Response(text='12345')


async def add_user(request):
    json_data = await request.json()
    await add_user_to_db(request.app['conn'],
                         json_data['name'],
                         json_data['lon'],
                         json_data['lat'])
    return web.Response(text='Added')


async def get_neighbors(request):
    params = request.rel_url.query
    users_data = await get_neighbors_from_db(request.app['conn'])
    return web.Response(text=str(users_data))
