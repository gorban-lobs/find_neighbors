import asyncio
import aiomysql


async def establish_connection():
    connection = await aiomysql.connect(
        unix_socket="/var/run/mysqld/mysqld.sock",
        user='hukuta',
        password='',
        db='find_neighbors')
    return connection


async def get_all_users(conn):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * from users;')
        users_data = await cur.fetchall()
    return users_data


async def add_user_to_db(conn, name, lon, lat):
    async with conn.cursor() as cur:
        sql_query = '''INSERT INTO users (name, lon, lat)
                    VALUES (%s, %s, %s)'''
        await cur.execute(sql_query, (name, lon, lat))
        await cur.execute('SELECT LAST_INSERT_ID();')
        user_id = await cur.fetchone()
        await conn.commit()
    return user_id[0]
