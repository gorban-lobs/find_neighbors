from handlers import show, get_neighbors


def setup_routes(app):
    app.router.add_get('/', show)
    app.router.add_get('/lookup', get_neighbors)
