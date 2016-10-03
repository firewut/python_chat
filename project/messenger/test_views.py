from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

import exceptions
import main
import utils


class AppTestCase(AioHTTPTestCase):

    def get_app(self, loop):
        app = main.get_application(loop)
        return app

    @unittest_run_loop
    async def test_index_view(self):
        request = await self.client.request(
            "GET",
            "/"
        )
        assert request.status == 200
        text = await request.text()
        assert "Welcome!" in text

    @unittest_run_loop
    async def test_user_view_get_no_session(self):
        request = await self.client.request(
            "GET",
            "/users"
        )
        assert request.status == 401

    @unittest_run_loop
    async def test_user_view_delete_no_session(self):
        request = await self.client.request(
            "DELETE",
            "/users"
        )
        assert request.status == 401

    @unittest_run_loop
    async def test_user_view_post(self):
        request = await self.client.request(
            "POST",
            "/users"
        )
        assert request.status == 200

    @unittest_run_loop
    async def test_user_view_get_self(self):
        name = utils.id_generator()
        request, session_id = await self.signup(name)
        assert request.status == 200
        request = await self.client.request(
            "GET",
            "/users",
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        assert request.status == 200
        json_text = await request.json()
        assert json_text['name'] == name

    @unittest_run_loop
    async def test_user_view_delete_with_session(self):
        request, session_id = await self.signup()
        assert request.status == 200
        request = await self.logout(session_id=session_id)
        assert request.status == 204
        request = await self.logout(session_id=session_id)
        assert request.status == 204
        # assert request.status == 401

    @unittest_run_loop
    async def test_chats_view_get_no_session(self):
        request = await self.client.request(
            "GET",
            "/chats"
        )
        assert request.status == 401

    @unittest_run_loop
    async def test_chats_view_get(self):
        request, session_id = await self.signup()
        assert request.status == 200
        request = await self.client.request(
            "GET",
            "/chats",
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        assert request.status == 200
        json = await request.json()
        assert len(json) == 0

    @unittest_run_loop
    async def test_chats_view_post_without_members(self):
        request, session_id = await self.signup()
        assert request.status == 200
        data = {
            "members": []
        }
        request = await self.client.request(
            "POST",
            "/chats",
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        assert request.status == 422
        text = await request.text()
        assert str(exceptions.ChatMembersRequired) in text

    @unittest_run_loop
    async def test_chats_view_post_with_non_existing_members(self):
        request, session_id = await self.signup()
        assert request.status == 200
        data = {
            "members": [
                utils.id_generator(10),
                utils.id_generator(10),
            ]
        }
        request = await self.client.request(
            "POST",
            "/chats",
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        assert request.status == 422
        text = await request.text()
        assert str(exceptions.UserDoesNotExist) in text

    @unittest_run_loop
    async def test_chats_view_post_with_existing_member(self):
        request, session_id = await self.signup()
        assert request.status == 200
        data = {
            "members": [
                'bot',
                'mark',
            ]
        }
        request = await self.client.request(
            "POST",
            "/chats",
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        json_text = await request.json()
        assert request.status == 201
        assert 'members' in json_text

        bot_in_members = False
        for member in json_text['members']:
            if 'bot' in member['name']:
                bot_in_members = True
        assert bot_in_members == True

    @unittest_run_loop
    async def test_chats_view_post_with_existing_members(self):
        user_name = utils.id_generator(100)
        request, session_id = await self.signup(name=user_name)
        assert request.status == 200
        data = {
            "members": [
                'bot', 
                'veronika',
            ]
        }
        request = await self.client.request(
            "POST",
            "/chats",
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        json_text = await request.json()
        assert request.status == 201
        assert 'members' in json_text

        bot_in_members = False
        self_in_members = False
        for member in json_text['members']:
            if 'bot' in member['name']:
                bot_in_members = True
            if user_name in member['name']:
                self_in_members = True
        assert bot_in_members == True
        assert self_in_members == True


        # Switch members
        data = {
            "members": [
                'bot', 
                user_name,
                'veronika',
            ]
        }
        request = await self.client.request(
            "POST",
            "/chats",
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        assert request.status == 409

    # @unittest_run_loop
    # async def test_chats_view_delete_existing(self):
    #     request, session_id = await self.signup()
    #     assert request.status == 201
    #     request = await self.register_chat(session_id=session_id)
    #     assert request.status == 201

    @unittest_run_loop
    async def test_chats_view_get(self):
        request, session_id = await self.signup()
        assert request.status == 200
        request, json_text = await self.register_chat(session_id=session_id)
        assert request.status == 201
        request = await self.get_chats(session_id=session_id)
        json = await request.json()
        assert len(json) > 0

    @unittest_run_loop
    async def test_chat_view_get(self):
        request, session_id = await self.signup()
        assert request.status == 200
        request, json_text = await self.register_chat(session_id=session_id)
        assert request.status == 201

        request = await self.get_chat(chat_id=json_text['id'], session_id=session_id)
        json_text_II = await request.json()
        assert json_text == json_text_II

    @unittest_run_loop
    async def test_chat_view_delete(self):
        request, session_id = await self.signup()
        assert request.status == 200
        request, json_text = await self.register_chat(session_id=session_id)
        assert request.status == 201

        request = await self.delete_chat(chat_id=json_text['id'], session_id=session_id)
        assert request.status == 204

    @unittest_run_loop
    async def test_chat_view_send_message_via_post(self):
        request, session_id = await self.signup()
        assert request.status == 200
        request, json_text = await self.register_chat(session_id=session_id)
        assert request.status == 201

        chat_id = json_text['id']
        message = utils.id_generator(100)
        request = await self.send_message(chat_id=chat_id, message=message, session_id=session_id)
        assert request.status == 201

    @unittest_run_loop
    async def test_chat_view_send_message_via_put(self):
        request, session_id = await self.signup()
        assert request.status == 200
        request, json_text = await self.register_chat(session_id=session_id)
        assert request.status == 201

        chat_id = json_text['id']

        # Write a few messages
        for i in range(1, 5, 1):
            message = utils.id_generator(100)
            request = await self.send_message_via_put(
                chat_id=chat_id,
                message=message,
                session_id=session_id
            )
            assert request.status == 201

    @unittest_run_loop
    async def test_message_view_send_message_to_user(self):
        member_I = utils.id_generator()
        request, session_I = await self.signup(member_I)
        assert request.status == 200

        member_II = utils.id_generator()
        request, session_II = await self.signup(member_II)
        assert request.status == 200

        recipients = ['bot', member_I]

        # Write a few messages
        for i in range(1, 5, 1):
            message = utils.id_generator(100)
            request = await self.send_mesage_to_users(
                recipients=recipients,
                message=message,
                session_id=session_II
            )
            assert request.status == 200
            json_text = await request.json()
            assert 'id' in json_text

        # Get a created chats
        request = await self.get_chats(session_id=session_I)
        assert request.status == 200
        json_text = await request.json()

        chat_members = recipients[:]
        chat_members.append(member_II)
        chat_found = False
        for chat in json_text:
            if chat['name'] == ','.join(
                sorted(chat_members)
            ):
                chat_found = True
                assert 'last_message' in chat
                assert chat['last_message']['message'] == message
        assert chat_found == True

    @unittest_run_loop
    async def test_messages_view_get(self):
        member_I = utils.id_generator()
        request, session_I = await self.signup(member_I)
        assert request.status == 200

        member_II = utils.id_generator()
        request, session_II = await self.signup(member_II)
        assert request.status == 200

        recipients = ['bot', member_I]

        # Write a few messages
        chat_id = ""
        for i in range(1, 5, 1):
            message = utils.id_generator(100)
            request = await self.send_mesage_to_users(
                recipients=recipients,
                message=message,
                session_id=session_I
            )
            assert request.status == 200
            json_text = await request.json()
            assert 'id' in json_text
            chat_id = json_text['id']

        request = await self.get_messages_from_chat(
            chat_id=chat_id,
            session_id=session_I
        )
        assert request.status == 200
        json_text = await request.json()

        message_found = False
        for message_json in json_text:
            if message_json['message'] == message:
                message_found = True
        assert message_found == True

    @unittest_run_loop
    async def test_contact_search(self):
        name = utils.id_generator()
        request, session_id = await self.signup(name)
        assert request.status == 200

        request = await self.client.request(
            "GET",
            "/users?name=vero",
            headers={
                "Authorization": "SessionId %s" % session_id,
            },
        )
        assert request.status == 200
        json_text = await request.json()
        for u in json_text:
            assert 'veronika' in u['name']



    # Helpers
    async def signup(self, name=None):
        data = None
        if name:
            data = {"name": name}
        request = await self.client.request(
            "POST",
            "/users",
            data=data
        )
        session_id = None
        try:
            json_text = await request.json()
            session_id = json_text['SessionId']
        except:
            pass

        return request, session_id

    async def logout(self, session_id):
        return await self.client.request(
            "DELETE",
            "/users",
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )

    async def register_chat(self, name=None, members=['bot', 'mark'], session_id=''):
        data = {
            "members": members
        }
        request = await self.client.request(
            "POST",
            "/chats",
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
        json_text = await request.json()
        assert request.status == 201
        assert 'members' in json_text

        bot_in_members = False
        for member in json_text['members']:
            if 'bot' in member['name']:
                bot_in_members = True
        assert bot_in_members == True
        return request, json_text

    async def get_chats(self, session_id):
        return await self.client.request(
            "GET",
            "/chats",
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )

    async def get_chat(self, chat_id, session_id):
        return await self.client.request(
            "GET",
            "/chats/%s" % chat_id,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )

    async def delete_chat(self, chat_id, session_id):
        return await self.client.request(
            "DELETE",
            "/chats/%s" % chat_id,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )

    async def send_message(self, chat_id, message, session_id):
        data = {
            "message": message
        }
        return await self.client.request(
            "POST",
            "/chats/%s" % chat_id,
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )

    async def send_message_via_put(self, chat_id, message, session_id):
        data = {
            "message": message
        }
        return await self.client.request(
            "PUT",
            "/chats/%s" % chat_id,
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )

    async def send_mesage_to_users(self, recipients, message, session_id):
        data = {
            "recipients": recipients,
            "message": message
        }
        return await self.client.request(
            "PUT",
            "/message",
            data=data,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )

    async def get_messages_from_chat(self, chat_id, session_id):
        return await self.client.request(
            "GET",
            "/chats/%s/messages" % chat_id,
            headers={
                "Authorization": "SessionId %s" % session_id,
            }
        )
