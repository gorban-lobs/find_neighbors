from from find_neighbors.handlers import get_neighbors, add_user


def setup_routes(app):
    app.router.add_get('/lookup', get_neighbors)
    app.router.add_post('/users', add_user)
