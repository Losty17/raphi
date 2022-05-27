import sqlalchemy
import enum
from typing import Final
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class VipEnum(enum.Enum):
    NONE = 0
    ONCE = 1
    MEGA = 2
    GIGA = 3
    TERA = 4


class NodeEnum(enum.Enum):
    WEB = 0
    DATA = 1
    DESIGN = 2
    CODING = 3
    NETWORK = 4
    ROBOTICS = 5
    HARDWARE = 6
    SOFTWARE = 7


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    web_bits = Column(Integer, default=0)
    data_bits = Column(Integer, default=0)
    design_bits = Column(Integer, default=0)
    coding_bits = Column(Integer, default=0)
    network_bits = Column(Integer, default=0)
    robotics_bits = Column(Integer, default=0)
    hardware_bits = Column(Integer, default=0)
    software_bits = Column(Integer, default=0)

    vip = Column(Enum(VipEnum), default=VipEnum.NONE)

    last_vote = Column(DateTime)

    def __repr__(self) -> str:
        return f"<User id={self.id}>"


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement='ignore_fk')

    node = Column(Enum(NodeEnum))
    text = Column(String(200))

    first_ans = Column(String(200))
    second_ans = Column(String(200))
    third_ans = Column(String(200))
    fourth_ans = Column(String(200))
    right_ans = Column(String(200))

    def __repr__(self) -> str:
        return f"<Question id={self.id} node={self.node}>"
