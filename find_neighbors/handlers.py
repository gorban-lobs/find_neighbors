import json
from aiohttp import web

from db_logic import add_user_to_db, get_neighbors_by_ids


async def add_user(request):
    try:
        json_data = await request.json()
        lon = float(json_data['lon'])
        lat = float(json_data['lat'])
        name = str(json_data['name'])
    except json.decoder.JSONDecodeError:
        return web.Response(text='No json data')
    except KeyError:
        return web.Response(text='Wrong number of parameters')
    except ValueError:
        return web.Response(text='Wrong parameter type')

    user_id = await add_user_to_db(request.app['conn'], name, lon, lat)
    request.app['index'].add_items([[lon, lat]], user_id)
    return web.Response(text='Added')


async def get_neighbors(request):
    index_size = len(request.app['index'].get_ids_list())
    if index_size == 0:
        return web.Response(text='There is no users in database')

    params = request.rel_url.query
    try:
        lon = float(params['lon'])
        lat = float(params['lat'])
        radius = int(params['radius'])
        limit = int(params['limit'])
    except KeyError:
        return web.Response(text='Wrong number of parameters')
    except ValueError:
        return web.Response(text='Wrong parameter type')

    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        return web.Response(text='Wrong coordinates')

    if limit > index_size:
        return web.Response(text=f'Limit must be <= {index_size}')

    ids = request.app['index'].search_neighbors(lon, lat, radius, limit)
    if ids.size == 0:
        return web.Response(text='No neighbors in such radius')

    str_ids = [str(id) for id in ids]
    neighbors = await get_neighbors_by_ids(request.app['conn'], str_ids)
    result = [''] * len(neighbors)
    for nbr in neighbors:
        result[str_ids.index(str(nbr[0]))] = nbr[1]
    return web.Response(text=str(result))
