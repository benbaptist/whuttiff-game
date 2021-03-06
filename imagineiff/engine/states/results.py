import time

class StateResults:
    def __str__(self):
        return "results"

    @property
    def json(self):
        return {
            "question": {
                "text": self.question.text,
                "options": self.question.options
            },
            "answers": self.question.answers,
            "duration": self.duration,
            "winning_answers": self.winning_answers,
            "winners": self.winners,
            "tally": self.tally
        }

    @property
    def tally(self):
        return self.question.tally

    @property
    def winning_answers(self):
        return self.question.winning_answers

    @property
    def winners(self):
        return self.question.winners

    @property
    def duration(self):
        return time.time() - self.time

    @property
    def question_text(self):
        return \
            self.question["question"].replace("__name__", self.about.name)

    def __init__(self, question):
        self.question = question

        self.time = time.time()
