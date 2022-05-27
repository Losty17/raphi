from sqlalchemy import create_engine
from .models import *


class Database:
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///data.db', echo=True)

    def sync(self):
        Quest.metadata.create_all(self.engine)
        Usr.metadata.create_all(self.engine)
