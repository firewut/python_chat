from aiohttp import web

import aiohttp_jinja2
import base64
import jinja2


import middlewares
import routes
import models
import server

async def on_shutdown(app):
    if 'websockets' in app:
        for ws in app['websockets']:
            await ws.close(code=999, message='Server shutdown')

async def on_prepare(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization'


def get_application(loop=None):
    app = web.Application(
        loop=loop,
    )
    # This is where live things happening
    app['server'] = server.Server(loop)

    # Attach middlwares
    app.middlewares.append(middlewares.auth_middleware_factory)

    # Attach Jinja2 Templates
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader('templates')
    )
    # Attach routes
    routes.setup_routes(app, ".")
    app.router.add_static('/static', 'static', name='static')

    # Sync models
    models.db_connection.sync()

    app.on_shutdown.append(on_shutdown)
    app.on_response_prepare.append(on_prepare)

    return app
