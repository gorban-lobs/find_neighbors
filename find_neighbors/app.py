import json
import asyncio
from aiohttp import web

from find_neighbors.routes import setup_routes
from find_neighbors.db_logic import establish_connection
from find_neighbors.db_logic import get_all_users, create_table
from find_neighbors.search_logic import NeighborIndex


async def init_app():
    app = web.Application()

    settings = json.load(open('settings.json', 'r'))
    conn = await establish_connection(settings['db'])
    app['conn'] = conn
    await create_table(conn)

    users = await get_all_users(conn)
    app['index'] = NeighborIndex(users)

    setup_routes(app)
    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app)
