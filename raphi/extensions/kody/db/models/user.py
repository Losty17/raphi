from sqlalchemy import BigInteger, Column, Integer, Enum, DateTime, String, text
from .enums import NodeEnum, VipEnum
from raphi.db.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)

    web_bits = Column(Integer, server_default='0')
    data_bits = Column(Integer, server_default='0')
    design_bits = Column(Integer, server_default='0')
    coding_bits = Column(Integer, server_default='0')
    network_bits = Column(Integer, server_default='0')
    robotics_bits = Column(Integer, server_default='0')
    hardware_bits = Column(Integer, server_default='0')
    software_bits = Column(Integer, server_default='0')

    vip = Column(Enum(VipEnum), server_default=VipEnum.none.name)

    last_vote = Column(DateTime)
    last_question = Column(DateTime)

    def __repr__(self) -> str:
        return f"<User id={self.id}>"

    def update_node(self, node: str):
        match node:
            case NodeEnum.web.name:
                self.web_bits += 1
            case NodeEnum.data.name:
                self.data_bits += 1
            case NodeEnum.design.name:
                self.design_bits += 1
            case NodeEnum.coding.name:
                self.coding_bits += 1
            case NodeEnum.network.name:
                self.network_bits += 1
            case NodeEnum.robotics.name:
                self.robotics_bits += 1
            case NodeEnum.hardware.name:
                self.hardware_bits += 1
            case NodeEnum.software.name:
                self.software_bits += 1
            case _:
                raise ValueError("Node type must be one of NodeEnum items")

    def get_rank(self) -> int:
        pass
