from enum import Enum


class VipEnum(Enum):
    none = "none"
    once = "once"
    mega = "mega"
    giga = "giga"
    tera = "tera"


class NodeEnum(Enum):
    __order__: str = 'web data design coding network robotics hardware software'
    web: str = "web"
    data: str = "data"
    design: str = "design"
    coding: str = "coding"
    network: str = "network"
    robotics: str = "robotics"
    hardware: str = "hardware"
    software: str = "software"


