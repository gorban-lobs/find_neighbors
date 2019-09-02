from aiohttp import web

from db_logic import add_user_to_db, get_neighbors_by_ids


async def add_user(request):
    json_data = await request.json()
    user_id = await add_user_to_db(request.app['conn'],
                                   json_data['name'],
                                   float(json_data['lon']),
                                   float(json_data['lat']))
    request.app['index'].add_items([[float(json_data['lon']),
                                     float(json_data['lat'])]],
                                   user_id)
    return web.Response(text='Added')


async def get_neighbors(request):
    if len(request.app['index'].get_ids_list()) == 0:
        return web.Response(text='There is no users in database')

    params = request.rel_url.query
    lon = float(params['lon'])
    lat = float(params['lon'])
    radius = int(params['radius'])
    limit = int(params['limit'])

    ids = request.app['index'].search_neighbors(lon, lat, radius, limit)
    if ids.size == 0:
        return web.Response(text='No neighbors in such radius')

    str_ids = [str(id) for id in ids]
    neighbors = await get_neighbors_by_ids(request.app['conn'], str_ids)
    result = [''] * len(neighbors)
    for nbr in neighbors:
        result[str_ids.index(str(nbr[0]))] = nbr[1]
    return web.Response(text=str(result))
