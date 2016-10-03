from aiohttp import web
import aiohttp_jinja2
import datetime

import models
import utils
import exceptions
from urllib.parse import parse_qs


class IndexHandler(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return


class MessageHandler(web.View):
    async def delete(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def get(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def patch(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def post(self):
        return await self.put()

    async def put(self):
        if 'user_session' in self.request:
            sender = self.request["user"]
            data = await self.request.post()
            recipients = data.getall('recipients')
            if len(recipients) > 0:
                chat, err = sender.SendMessageToUsers(
                    recipients=recipients,
                    message_text=data.get('message', ''),
                )
                if err:
                    return web.Response(
                        text="422: %s" % str(err),
                        status=422
                    )
                else:
                    response = await chat.to_json()
                    return web.json_response(response, status=200)
            else:
                return web.Response(
                    text="422: Need a recipient",
                    status=422
                )

        return web.HTTPUnauthorized()

    async def options(self):
        headers = {'Allow': 'PUT,OPTIONS'}
        return web.Response(headers=headers)


class MessagesHandler(web.View):
    async def delete(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def get(self):
        if 'user_session' in self.request:
            c = models.Chat(id=self.request.match_info['id'])
            chat = c.FindOneForUser(
                user_id=self.request["user_session"].user_id,
            )
            if chat:
                query_params = {}
                if len(self.request.query_string) > 0:
                    query_params = parse_qs(self.request.query_string)

                response = []
                messages = chat.GetMessages(params=query_params)
                for message in messages:
                    response.append(await message.to_json())
                return web.json_response(response)
            else:
                return web.HTTPNotFound()
        return web.HTTPUnauthorized()

    async def post(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def put(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def patch(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def options(self):
        headers = {'Allow': 'GET,OPTIONS'}
        return web.Response(headers=headers)


class ChatHandler(web.View):
    async def delete(self):
        if 'user_session' in self.request:
            c = models.Chat(id=self.request.match_info['id'])
            chat = c.FindOneForUser(
                user_id=self.request["user_session"].user_id,
            )
            if chat:
                err = chat.Delete()
                if err == None:
                    return web.HTTPNoContent()
                else:
                    return web.Response(
                        text="422: %s" % str(err),
                        status=422
                    )
            else:
                return web.HTTPNotFound()
        return web.HTTPUnauthorized()

    async def get(self):
        if 'user_session' in self.request:
            c = models.Chat(id=self.request.match_info['id'])
            chat = c.FindOneForUser(
                user_id=self.request["user_session"].user_id,
            )
            if chat:
                response = await chat.to_json()
                return web.json_response(response)
            else:
                return web.HTTPNotFound()
        return web.HTTPUnauthorized()

    async def post(self):
        if 'user_session' in self.request:
            c = models.Chat(id=self.request.match_info['id'])
            chat = c.FindOneForUser(
                user_id=self.request["user_session"].user_id,
            )
            if chat:
                data = await self.request.post()

                query_params = {}
                if len(self.request.query_string) > 0:
                    query_params = parse_qs(self.request.query_string)
                    err = chat.AddMembers(
                        members=query_params.all('members')
                    )
                else:    
                    err = chat.SendMessage(
                        sender=self.request["user"],
                        message_text=data.get('message', ''),
                    )
                if err == None:
                    return web.HTTPCreated()
                else:
                    return web.Response(
                        text="422: %s" % str(err),
                        status=422
                    )
            else:
                return web.HTTPNotFound()
        return web.HTTPUnauthorized()

    async def put(self):
        return await self.post()

    async def patch(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def options(self):
        headers = {'Allow': 'GET,POST,DELETE,OPTIONS'}
        return web.Response(headers=headers)



class ChatsHandler(web.View):
    async def delete(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def patch(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def put(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def options(self):
        headers = {'Allow': 'GET,POST,OPTIONS'}
        return web.Response(headers=headers)

    async def get(self):
        if self.request.get("user"):
            c = models.Chat()
            chats = c.FindAllForUser(
                user_id=self.request["user_session"].user_id
            )
            response = []
            for chat in chats:
                response.append(await chat.to_json())
            return web.json_response(response)
        return web.HTTPUnauthorized()

    async def post(self):
        user = self.request.get("user")
        if user:
            data = await self.request.post()

            c = models.Chat()
            chat, err = c.Create(
                creator=user,
                name=data.get('name', ''),
                raw_members=data.getall('members', [])
            )
            if err == None:
                response = await chat.to_json()
                return web.json_response(response, status=201)
            else:
                if err == exceptions.ChatWithMembersAlreadyExists:
                    return web.HTTPConflict()
                else:
                    return web.Response(
                        text="422: %s" % str(err),
                        status=422
                    )
        return web.HTTPUnauthorized()


class UsersHandler(web.View):
    async def delete(self):
        if 'user_session' in self.request:
            err = await self.request['user_session'].Delete()
            if err == None:
                return web.HTTPNoContent()
            else:
                return web.Response(
                    text="422: %s" % str(err),
                    status=422
                )
        return web.HTTPUnauthorized()

    async def get(self):
        if 'user_session' in self.request:
            query_params = {}
            if len(self.request.query_string) > 0:
                query_params = parse_qs(self.request.query_string)
                u = models.User()
                users = await u.Search(params=query_params)
                response = []
                for u in users:
                    response.append(await u.to_json())
            else:
                response = await self.request['user'].to_json()

            return web.json_response(response)
        return web.HTTPUnauthorized()

    async def post(self):
        """
            Register new user
        """
        data = await self.request.post()

        new_user = models.User()
        created_session, err = new_user.Signup(
            data,
        )

        if err == None:
            session = {}
            try:
                session = await get_session(self.request)
            except:
                pass

            session['session_key'] = created_session.id

            return web.json_response({
                "SessionId": created_session.id
            })
        else:
            if err == exceptions.UserAlreadyExists:
                return web.HTTPConflict()
            else:
                self.request.app.logger.error(err)
                return web.Response(
                    text="422: %s" % str(err),
                    status=422
                )

        return web.HTTPInternalServerError()

    async def patch(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def put(self):
        if 'user_session' in self.request:
            return web.HTTPNotImplemented()
        return web.HTTPUnauthorized()

    async def options(self):
        headers = {'Allow': 'GET,DELETE,POST,OPTIONS'}
        return web.Response(headers=headers)