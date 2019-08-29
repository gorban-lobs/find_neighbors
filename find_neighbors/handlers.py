from aiohttp import web

from db_logic import add_user_to_db


async def show(request):
    return web.Response(text='12345')


async def add_user(request):
    json_data = await request.json()
    await add_user_to_db(request.app['conn'],
                         json_data['name'],
                         json_data['lon'],
                         json_data['lat'])
    user_ind = 6 # get user index
    request.app['index'].add_items([json_data['lon'], json_data['lat']],
                                   user_ind)
    return web.Response(text='Added')


async def get_neighbors(request):
    params = request.rel_url.query
    neighbors = request.app['index'].search_neighbors(
        float(params['lon']), float(params['lat']),
        int(params['radius']), int(params['limit']))
    return web.Response(text=str(neighbors))
