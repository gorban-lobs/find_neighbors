from handlers import show


def setup_routes(app):
    app.router.add_get('/', show)
