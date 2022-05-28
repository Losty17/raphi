from typing import List


class Question:
    def __init__(self, answers: List[str], right_answer: str, content: str) -> None:
        self.answers = answers
        self.right_answer = right_answer
        self.content = content

    @classmethod
    def get_question(self, answers: List[str], right_answer: str, content: str):
        return Question(answers, right_answer, content) if right_answer in answers else None
