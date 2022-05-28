from sqlalchemy import text, select, update, values
from .models import Question, User
from raphi.db import DatabaseCore


class KodyDatabase(DatabaseCore):
    def __init__(self) -> None:
        super().__init__()

    def create_user(self, _id: int) -> bool:
        try:
            with self.session.begin():
                user = User(id=_id)
                self.session.add(user)
        except Exception as e:
            return False, e
        else:
            return True

    def get_user(self, _id: int) -> User | None:
        with self.session.begin():
            user = self.session.query(User).filter_by(id=_id).first()
        return user

    def update_user_last_question(self, user: User) -> bool:
        try:
            with self.session.begin():
                self.session.execute(
                    update(User)
                    .where(User.id == user.id)
                    .values(last_question=user.last_question)
                )
        except Exception as e:
            return False, e
        else:
            return True

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
            question = self.session.query(Question).filter_by(id=_id).first()

        return question

    def get_questions(self):
        with self.session.begin():
            questions = self.session.query(Question).all()

        return questions
