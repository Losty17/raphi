from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from . import Base


class DatabaseCore:
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
