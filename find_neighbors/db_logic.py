import asyncio
import aiomysql


async def establish_connection(settings):
    connection = await aiomysql.connect(
        host=settings['host'],
        port=settings['port'],
        user=settings['user'],
        password=settings['password'],
        db=settings['db'])
    return connection


async def create_table(conn):
    async with conn.cursor() as cur:
        sql_query = '''CREATE TABLE IF NOT EXISTS users (
            id int(11) NOT NULL AUTO_INCREMENT,
            name varchar(100) DEFAULT NULL,
            lon float DEFAULT NULL,
            lat float DEFAULT NULL,
            PRIMARY KEY (id)
            ) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1'''
        await cur.execute(sql_query)


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


async def get_neighbors_by_ids(conn, ids):
    async with conn.cursor() as cur:
        fmt_str = ','.join(['%s'] * len(ids))
        await cur.execute(f'SELECT id, name FROM users WHERE id IN ({fmt_str})',
                          ids)
        users = await cur.fetchall()
    return users
