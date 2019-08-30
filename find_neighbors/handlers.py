from aiohttp import web

from db_logic import add_user_to_db, get_neighbors_by_ids


async def show(request):
    return web.Response(text='12345')


async def add_user(request):
    json_data = await request.json()
    user_id = await add_user_to_db(request.app['conn'],
                                   json_data['name'],
                                   json_data['lon'],
                                   json_data['lat'])
    request.app['index'].add_items([json_data['lon'],
                                    json_data['lat']],
                                    user_id)
    return web.Response(text='Added')


async def get_neighbors(request):
    params = request.rel_url.query
    ids = request.app['index'].search_neighbors(
        float(params['lon']), float(params['lat']),
        int(params['radius']), int(params['limit']))
    str_ids = [str(id) for id in ids]
    neighbors = await get_neighbors_by_ids(request.app['conn'], str_ids)
    return web.Response(text=str(neighbors))
