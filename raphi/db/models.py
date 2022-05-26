from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)
