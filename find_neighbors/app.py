from aiohttp import web
import asyncio
import aiomysql

from routes import setup_routes
from db_logic import establish_connection


async def init_app():
    app = web.Application()
    conn = await establish_connection()
    app['conn'] = conn
    setup_routes(app)
    return app


app = init_app()
web.run_app(app)
