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
    cur_user = request.app.users.get(params['id'], 'No such user')
    return web.Response(text=str(cur_user))
