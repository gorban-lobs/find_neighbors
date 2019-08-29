import asyncio
import aiomysql
from aiohttp import web


async def show(request):
    return web.Response(text='12345')


async def add_user(request):
    json_data = await request.json()
    new_id = len(request.app.users) + 1
    request.app.users[str(new_id)] = {
        'name': json_data['name']
    }
    return web.Response(text='Added')


async def get_neighbors(request):
    params = request.rel_url.query
    conn = await aiomysql.connect(unix_socket="/var/run/mysqld/mysqld.sock",
                                      user='hukuta', password='',
                                      db='find_neighbors')
    cur = await conn.cursor()
    await cur.execute("SELECT * from users;")
    data = await cur.fetchall()
    await cur.close()
    conn.close()
    return web.Response(text=str(data))
