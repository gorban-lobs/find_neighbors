from aiohttp import web
import asyncio
import aiomysql

from routes import setup_routes
from db_logic import establish_connection, get_all_users, create_table
from search_logic import NeighborIndex


async def init_app():
    app = web.Application()
    conn = await establish_connection()
    app['conn'] = conn
    await create_table(conn)
    users = await get_all_users(conn)
    app['index'] = NeighborIndex(users)
    setup_routes(app)
    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app)
