from sqlalchemy import text
from .models import Question, User
from raphi.db import DatabaseCore


class KodyDatabase(DatabaseCore):
    def __init__(self) -> None:
        super().__init__()

    def create_user(self, _id: int):
        with self.engine.begin() as conn:
            q = text(f'INSERT INTO users (id) VALUES ({_id})')
            conn.execute(q)

        # return await self.session.query(User).filter_by(id=_id).first()

    def get_user(self, _id: int) -> User:
        with self.session.begin():
            return self.session.query(User).filter_by(id=_id).first()

    def insert_question(self, _text, node, right_ans, first_ans):
        with self.engine.begin() as conn:
            q = text(
                f'INSERT INTO questions' +
                f'(text, node, right_ans, first_ans)' +
                f"VALUES ('{_text}', '{node}', '{right_ans}', '{first_ans}')"
            )
            conn.execute(q)

    def get_question(self, _id: str) -> Question:
        with self.session.begin():
            return self.session.query(Question).filter_by(id=_id).first()

    def get_questions(self):
        with self.session.begin():
            return self.session.query(Question).all()
