from sqlalchemy import Column, Integer, String, Enum, DateTime
from .enums import NodeEnum
from ..base import Base


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
