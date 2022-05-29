from typing import List
from sqlalchemy import func
from .models import Question, User
from raphi.db import DatabaseCore


class KodyDatabase(DatabaseCore):
    def __init__(self) -> None:
        super().__init__()

    def create_user(self, user: User) -> User:
        with self.session.begin():
            self.session.add(user)

        return user

    def get_user(self, _id: int) -> User | None:
        with self.session.begin():
            user = self.session.query(User).filter_by(id=_id).first()

        return user

    def add_question(self, question: Question) -> Question:
        with self.session.begin():
            self.session.add(question)

        return question

    def bulk_add_question(self, questions: List[Question]):
        with self.session.begin():
            self.session.bulk_save_objects(questions)

    def get_question(self, _id: str) -> Question:
        with self.session.begin():
            question = self.session.query(Question).filter_by(id=_id).first()

        return question

    def get_questions(self):
        with self.session.begin():
            questions = self.session.query(Question).all()

        return questions

    def get_random_question(self) -> Question | None:
        with self.session.begin():
            questions = self.session.query(Question).order_by(
                func.random()).limit(1).one_or_none()

        return questions
