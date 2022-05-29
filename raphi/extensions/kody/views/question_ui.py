from random import shuffle
from discord import User

from discord.ui import View
from ..db.models import Question

from . import QuestionButton


class QuestionUi(View):
    def __init__(self, question: Question, *, author: User):
        super().__init__(timeout=60)

        answers = question.get_answers()
        right_ans = question.right_ans
        shuffle(answers)

        btns = []
        for i in answers:
            if i:
                btns.append(QuestionButton(
                    i, question.node.name, right_ans, btns, author=author))

        for btn in btns:
            self.add_item(btn)
