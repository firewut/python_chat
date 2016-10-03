import models

async def auth_middleware_factory(app, handler):
    async def middleware_handler(request):
        session_header = request.headers.get('Authorization')
        if session_header and 'SessionId ' in session_header:
            session_id = session_header.replace('SessionId ', '')
            user_session = await models.Session().Get(session_id)
            if user_session:
                request["user_session"] = user_session
                user = await models.User(id=user_session.user_id).Get()
                if user:
                    request["user"] = user
        return await handler(request)
    return middleware_handler
