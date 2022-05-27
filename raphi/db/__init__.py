import sqlalchemy
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine as create_engine, AsyncConnection
from .models import *


class Database:
    def __init__(self) -> None:
        # self.engine = create_engine('sqlite+aiosqlite:///:memory:', echo=True)
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.bind = self.engine
        Session = sessionmaker(bind=Base.metadata.bind)

        self.session = Session()

    def sync(self):
        with self.engine.begin() as conn:
            Base.metadata.drop_all()
            Base.metadata.create_all()
            # conn.run(Base.metadata.drop_all)
            # conn.execute(Base.metadata.create_all)

    def create_user(self, _id: int):
        with self.engine.begin() as conn:
            q = text(f'INSERT INTO users (id) VALUES ({_id})')
            conn.execute(q)

        # return await self.session.query(User).filter_by(id=_id).first()

    def get_user(self, _id: int) -> User:
        with self.session.begin():
            return self.session.query(User).filter_by(id=_id).first()
