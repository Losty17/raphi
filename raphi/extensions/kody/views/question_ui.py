from random import shuffle

from discord.ui import View
from ..question import Question

from . import QuestionButton


class QuestionUi(View):
    def __init__(self, question: Question):
        super().__init__(timeout=60)
        self.question = question
        shuffle(self.question.answers)
        right_ans = self.question.right_answer

        btns = []

        for i in question.answers:
            btns.append(QuestionButton(i, right_ans, btns, self))

        for btn in btns:
            self.add_item(btn)
