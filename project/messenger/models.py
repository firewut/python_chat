from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, joinedload, join, joinedload_all
from sqlalchemy import Column, String, Integer, \
    ForeignKey, DateTime, UnicodeText, Table, \
    Boolean
from sqlalchemy.dialects import postgresql


import datetime
import exceptions
import random
import sqlalchemy
import utils
import uuid

import db
import settings
db_connection = db.DbConnection()

Base = declarative_base(
    bind=db_connection.Conn,
    metadata=db_connection.Meta,
)


class Session(Base):
    __tablename__ = 'session'

    # , default=lambda: uuid.uuid4().hex )
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return "Session(id='%s', user='%s')" % (self.id, self.user_id)

    async def to_json(self):
        return dict(
            id=self.id,
            user=self.user
        )

    async def Get(self, session_id):
        db_session = db_connection.ScopedSession()

        s = None
        try:
            s = db_session.query(Session).get(session_id)
        except Exception as err:
            pass
        finally:
            db_session.close()
        return s

    async def Delete(self):
        db_session = db_connection.ScopedSession()
        err = None

        try:
            s = db_session.query(Session).filter_by(id=self.id).delete()
        except Exception as exc:
            err = exc
        finally:
            db_session.close()

        return err


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    message = Column(UnicodeText)

    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship(
        "User", foreign_keys=[sender_id], lazy='subquery', uselist=False)

    chat_id = Column(Integer, ForeignKey('chat.id'))

    def __repr__(self):
        return "Message(id='%s', sender='%s', chat='%s', date_created='%s')" % (
            self.id, self.sender_id, self.chat_id, self.date_created)

    __mapper_args__ = {
        "order_by": sqlalchemy.desc(id)
    }

    async def to_json(self):
        sender = await self.sender.to_json()

        return dict(
            id=self.id,
            message=self.message,
            sender=sender,
            date_created=self.date_created.isoformat()
        )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    avatar = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    date_recent_activity = Column(DateTime)

    def __repr__(self):
        return "User(id='%s', name='%s')" % (self.id, self.name)

    async def to_json(self):
        return dict(
            # id=self.id,
            name=self.name,
            date_created=self.date_created.isoformat(),
            avatar=self.avatar,
            date_recent_activity=self.date_recent_activity.isoformat()
        )

    def GetByName(self, one=True):
        db_session = db_connection.ScopedSession()

        users = None
        try:
            u = db_session.query(User).filter_by(name=self.name)
            if one:
                users = u.one()
            else:
                users = u.all()
        except Exception as err:
            pass
        finally:
            db_session.close()

        return users

    async def Search(self, params={}, limit=100):
        db_session = db_connection.ScopedSession()

        if limit > 100:
            limit = 100

        users = []
        try:
            query = db_session.query(User)
            # One of custom params
            if 'name' in params:
                name = params['name'][0]
                query = query.filter(User.name.ilike('%'+name+'%')) ## BEWARE SQL INJECTION
            
            users = query.all()
        except Exception as exc:
            err = exc
        finally:
            db_session.close()

        return users

    async def Get(self):
        db_session = db_connection.ScopedSession()

        u = None
        try:
            u = db_session.query(User).get(self.id)
        except Exception as err:
            pass
        finally:
            db_session.close()
        return u

    def SendMessageToUsers(self, recipients=[], message_text=''):
        """
            Find a Chat where members == [Sender, Recipient]
        """
        db_session = db_connection.ScopedSession()
        err = None

        # Check if there is a chat with user to receive a message
        c = Chat()
        members = recipients[:]
        members.append(self.name)
        chat, err = c.FindOneForUsers(
            members=members
        )
        if err == None:
            if chat == None:
                chat, err = c.Create(
                    creator=self,
                    name=','.join(
                        sorted(members)
                    ),
                    raw_members=recipients
                )

            if err == None:
                err = chat.SendMessage(
                    sender=self,
                    message_text=message_text,
                )
        return chat, err

    def Signup(self, data):
        db_session = db_connection.ScopedSession()
        err = None

        name = data.get('name', None)
        if name != None:
            # Must check existance
            try:
                if db_session.query(User).filter_by(name=name).count() > 0:
                    return None, exceptions.UserAlreadyExists
            except:
                pass

        else:
            name = utils.id_generator()

        now = datetime.datetime.utcnow()

        u = User()
        # u.id = str(uuid.uuid4().hex)
        u.name = name
        u.date_created = now
        u.date_recent_activity = now
        u.avatar = random.choice(settings.AVATARS)

        s = Session()
        try:
            db_session.add(u)
            db_session.flush()

            # Register session
            s.user_id = u.id
            db_session.add(s)
            db_session.commit()

            # Bot should greet new user
            b = User(name='bot').GetByName()
            if b:
                b.SendMessageToUsers(
                    recipients=[name],
                    message_text="Welcome, I'm bot. Ask me anything."
                )

        except Exception as exc:
            db_session.rollback()
            err = exc
        finally:
            db_session.close()

        return s, err


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    date_recent_activity = Column(DateTime)

    members = Column(postgresql.ARRAY(Integer))

    messages = relationship(
        'Message',
        backref="chat",
        cascade="all, delete-orphan",
        lazy='dynamic'
    )

    def __repr__(self):
        return "Chat(id='%s', name='%s')" % (
            self.id, self.name)

    __mapper_args__ = {
        "order_by": sqlalchemy.desc(date_recent_activity)
    }

    async def to_json(self):

        # TODO: Refactor this. Maybe we do not need to query all of it
        # Option 1: Make a list of fields to serialize and exclude
        #   from query those which are not in list
        user_members = []
        for member_id in self.members:
            u = User(id=member_id)
            user = await u.Get()
            if user:
                user_members.append(await user.to_json())

        # This is correct way - request most recent message
        last_message = None
        db_session = db_connection.ScopedSession()
        try:
            last_message_raw = db_session.query(Message).\
                filter_by(chat_id=self.id).order_by(
                    Message.id.desc()).limit(1).one()
            last_message = await last_message_raw.to_json()
        except Exception as exc:
            err = exc
        finally:
            db_session.close()

        return dict(
            id=self.id,
            name=self.name,
            date_created=self.date_created.isoformat(),
            last_message=last_message,
            members=user_members,
            date_recent_activity=self.date_recent_activity.isoformat()
        )

    def AddMembers(self, members=[]):
        db_session = db_connection.ScopedSession()
        err = None
        
        try:
            self.members.extend(members)
            db_session.commit()
        except Exception as exc:
            db_session.rollback()
            err = exc
        finally:
            db_session.close()

        return err

    def Find(self, **kwargs):
        db_session = db_connection.ScopedSession()
        filtered = db_session.query(Chat).filter(*kwargs)
        db_session.close()
        return filtered

    def FindAllForUser(self, user_id):
        db_session = db_connection.ScopedSession()
        chats = db_session.query(Chat).filter(
            Chat.members.contains([user_id])
        ).all()
        db_session.close()
        return chats

    def FindOneForUser(self, user_id):
        db_session = db_connection.ScopedSession()
        chat = db_session.query(Chat).filter(
            Chat.members.contains([user_id]),
            Chat.id == self.id,
        ).one()
        db_session.close()
        return chat

    def FindOneForUsers(self, members=[]):
        db_session = db_connection.ScopedSession()
        err = None

        raw_members = members[:]
        users = []
        try:
            if len(raw_members) == 0:
                return None, exceptions.ChatMembersRequired
            else:
                # Must select all members
                for member_name in raw_members:
                    u = User(name=member_name).GetByName()
                    if u:
                        users.append(
                            u,
                        )
                    else:
                        return None, exceptions.UserDoesNotExist
        except:
            pass

        try:
            chat = db_session.query(Chat).filter(
                Chat.members.contains([m.id for m in users]),
            ).one()
        except sqlalchemy.orm.exc.NoResultFound:
            chat = None

        db_session.close()
        return chat, err

    def GetMessages(self, params={}, limit=100):
        db_session = db_connection.ScopedSession()

        if limit > 100:
            limit = 100

        messages = []
        try:
            query = db_session.query(Message).filter(
                Message.chat_id == self.id,
            )
            # One of custom params
            if 'since_id' in params:
                since_id = params['since_id'][0]
                query = query.filter(Message.id > since_id)
            
            messages = query.all()
        except Exception as exc:
            err = exc
        finally:
            db_session.close()

        return messages

    def SendMessage(self, sender=None, message_text=""):
        if len(message_text) > 0:
            db_session = db_connection.ScopedSession()
            err = None

            message = Message(
                message=message_text,
                sender=sender,
                chat=self,
            )

            try:
                db_session.add(message)
                db_session.flush()

                self.date_recent_activity = datetime.datetime.utcnow()
                self.messages.append(message)

                db_session.commit()
            except Exception as exc:
                db_session.rollback()
                err = exc
            finally:
                db_session.close()
        return err

    def Delete(self):
        db_session = db_connection.ScopedSession()
        err = None

        try:
            db_session.query(Chat).filter_by(id=self.id).delete()
            db_session.commit()
        except Exception as exc:
            db_session.rollback()
            err = exc
        finally:
            db_session.close()
        return err

    def Create(self, creator, name="", raw_members=[]):
        # Must find a chat for these members
        lookup_members = raw_members[:]
        lookup_members.append(creator.name)

        if len(raw_members) == 0:
            return None, exceptions.ChatMembersRequired

        c, err = self.FindOneForUsers(members=lookup_members)
        if err == None:
            if c != None:
                return None, exceptions.ChatWithMembersAlreadyExists
            else:
                db_session = db_connection.ScopedSession()
                err = None

                members = []
                try:
                    if len(raw_members) == 0:
                        return None, exceptions.ChatMembersRequired
                    else:
                        # Must select all members
                        for member_name in raw_members:
                            u = User(name=member_name).GetByName()
                            if u:
                                members.append(
                                    u.id,
                                )
                            else:
                                return None, exceptions.UserDoesNotExist
                except:
                    pass

                if len(members) == 0:
                    return None, exceptions.ChatMembersRequired

                if len(name) == 0:
                    name = ",".join(
                        sorted(lookup_members)
                    )

                # This will append creator to a list of members
                if creator.id not in members:
                    members.append(
                        creator.id
                    )
                # Must check chat with members and name existance
                chats = db_session.query(Chat).filter(
                    Chat.members.contains(members),
                ).count()

                c = None
                if chats == 0:
                    try:
                        c = Chat(
                            name=name,
                            date_recent_activity=datetime.datetime.utcnow(),
                            members=members,
                            messages=[],
                        )
                        db_session.add(c)
                        db_session.commit()
                    except Exception as exc:
                        db_session.rollback()
                        err = exc
                    finally:
                        db_session.close()

        return c, err
