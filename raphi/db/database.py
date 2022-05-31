from os import getenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session as s
from sqlalchemy.orm import sessionmaker

from . import Base


class DatabaseCore:
    def __init__(self) -> None:
        db_uri = getenv("DATABASE_URI") if getenv(
            "ENVIRONMENT").lower() == "production" else "sqlite:///:memory:"
        self.engine = create_engine(db_uri)
        Base.metadata.bind = self.engine
        Session = sessionmaker(bind=Base.metadata.bind, autocommit=True)

        self.session: s = Session()

    def sync(self):
        with self.engine.begin() as conn:
            Base.metadata.drop_all()
            Base.metadata.create_all()
            # conn.run(Base.metadata.drop_all)
            # conn.execute(Base.metadata.create_all)
