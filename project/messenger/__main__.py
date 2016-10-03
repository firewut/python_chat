from aiohttp import web

import main

if __name__ == '__main__':
    app = main.get_application()
    web.run_app(app)
