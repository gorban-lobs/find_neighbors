from aiohttp import web

from routes import setup_routes


app = web.Application()
setup_routes(app)
app.users = {'1': {'name': 'Vasya'},
             '2': {'name': 'Petya'}}

web.run_app(app)
