from typing import List
from sqlalchemy import Column, Integer, String, Enum, DateTime
from .enums import NodeEnum
from raphi.db.base import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)

    node = Column(Enum(NodeEnum), nullable=False)
    text = Column(String(200), nullable=False)

    right_ans = Column(String(200), nullable=False)
    first_ans = Column(String(200), nullable=False)
    second_ans = Column(String(200), server_default='')
    third_ans = Column(String(200), server_default='')

    def __repr__(self) -> str:
        return f"<Question id={self.id} node={self.node}>"

    def get_answers(self) -> List[str]:
        return [self.right_ans, self.first_ans, self.second_ans, self.third_ans]
