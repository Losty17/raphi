from sqlalchemy import Column, Integer, Enum, DateTime
from .enums import VipEnum
from ..base import Base


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
