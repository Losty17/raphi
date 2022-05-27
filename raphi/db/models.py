import sqlalchemy
import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import declarative_base

Quest = declarative_base()
Usr = declarative_base()


class VipEnum(enum.Enum):
    none = 0
    mega = 1
    giga = 2
    tera = 3


class NodeEnum(enum.Enum):
    web = 0
    data = 1
    design = 2
    coding = 3
    network = 4
    robotics = 5
    hardware = 6
    software = 7


class User(Usr):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)

    web_bits = Column(Integer, default=0)
    data_bits = Column(Integer, default=0)
    design_bits = Column(Integer, default=0)
    coding_bits = Column(Integer, default=0)
    network_bits = Column(Integer, default=0)
    robotics_bits = Column(Integer, default=0)
    hardware_bits = Column(Integer, default=0)
    software_bits = Column(Integer, default=0)

    vip = Column(Enum(VipEnum), default=VipEnum.none)

    last_vote = Column(DateTime)

    def __repr__(self) -> str:
        return f"<User id={self.id}>"


class Question(Quest):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)

    node = Column(Enum(NodeEnum))
    text = Column(String(200))

    first_ans = Column(String(200))
    second_ans = Column(String(200))
    third_ans = Column(String(200))
    fourth_ans = Column(String(200))
    right_ans = Column(String(200))

    def __repr__(self) -> str:
        return f"<Question id={self.id} node={self.node}>"
