from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils.functions import *
from sqlalchemy import create_engine
import sqlalchemy

import os
import utils
import settings

USER = os.environ.get('DB_USER', 'postgres')
PASSWORD = os.environ.get('DB_PASSWORD', '123')

DB_CONN_URL = os.environ.get(
    'DB_CONN_URL', 'postgresql+psycopg2://postgres:123@localhost:32769')
DB_NAME = os.environ.get('DB_NAME', 'test_task_3_%s' % utils.id_generator(5))
PORT = os.environ.get('PORT', 32769)
HOST = os.environ.get('HOST', 'localhost')

class DbConnection(object):
    Conn = None
    Meta = None
    SessionFactory = None
    ScopedSession = None

    def _connect(self, user, password, db, host, port=5432):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)

        print("Connecting...", db)
        engine = create_engine(url)
        if not database_exists(engine.url):
            create_database(engine.url)

        self.Conn = create_engine(url, client_encoding='utf8')
        self.Meta = sqlalchemy.MetaData(bind=self.Conn, reflect=True)

    def __init__(self, user=USER, password=PASSWORD, db_name=DB_NAME, host=HOST, port=PORT):
        self._connect(user, password, db_name, host, port)
        self.SessionFactory = sessionmaker(
            bind=self.Conn,
            autocommit=False,
            expire_on_commit=False
        )
        self.ScopedSession = scoped_session(self.SessionFactory)
        return

    def sync(self):
        self.Meta.create_all(self.Conn, checkfirst=True)
        
        import models
        u = models.User()
        u.Signup(data={"name": "bot"})
        for avatar in settings.AVATARS:
            name = os.path.basename(os.path.splitext(avatar)[0])
            u.Signup(data={"name": name})
            
