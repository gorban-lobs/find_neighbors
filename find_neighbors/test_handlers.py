import pytest
from aiohttp import web

from find_neighbors.search_logic import NeighborIndex
from find_neighbors.handlers import add_user, get_neighbors


async def test_get_neighbors(aiohttp_client, aiohttp_server):
    app = web.Application()
    app['index'] = NeighborIndex([])
    app.router.add_get('/lookup', get_neighbors)

    client = await aiohttp_client(app)

    resp = await client.get('/lookup?lon=32.1')
    text = await resp.text()
    assert 'There is no users in database' == text

    app['index'].add_items([[11.1, 22.2]], [1])

    resp = await client.get('/lookup?lon=32.1')
    text = await resp.text()
    assert 'Wrong number of parameters' == text

    resp = await client.get('/lookup?lon=32.1&lat=abc&radius=1000&limit=1')
    text = await resp.text()
    assert 'Wrong parameter type' == text

    resp = await client.get('/lookup?lon=232.1&lat=-50.0&radius=1000&limit=1')
    text = await resp.text()
    assert 'Wrong coordinates' == text

    resp = await client.get('/lookup?lon=32.1&lat=-50.0&radius=1000&limit=20')
    text = await resp.text()
    assert 'Limit must be <= 1' == text

    resp = await client.get('/lookup?lon=32.1&lat=-50.0&radius=1&limit=1')
    text = await resp.text()
    assert 'No neighbors in such radius' == text


async def test_add_user(aiohttp_client, aiohttp_server):
    app = web.Application()
    app['index'] = NeighborIndex([])
    app.router.add_post('/users', add_user)

    client = await aiohttp_client(app)

    resp = await client.post('/users')
    text = await resp.text()
    assert text == 'No json data'

    resp = await client.post('/users', json={'lat': 11.1})
    text = await resp.text()
    assert text == 'Wrong number of parameters'

    resp = await client.post('/users', json={'lon': 11.1,
                                             'lat': 'abc',
                                             'name': 'Vasya'})
    text = await resp.text()
    assert text == 'Wrong parameter type'
