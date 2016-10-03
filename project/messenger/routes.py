from views import *


def setup_routes(app, project_root):
    app.router.add_route('*', '/', IndexHandler)
    app.router.add_route('*', '/users', UsersHandler)
    app.router.add_route('*', '/chats', ChatsHandler)
    app.router.add_route('*', '/chats/{id}', ChatHandler)
    app.router.add_route('*', '/chats/{id}/messages', MessagesHandler)
    app.router.add_route('*', '/message', MessageHandler)
