import time

class StateQuestion:
    def __str__(self):
        return "question"

    def __init__(self, question, tta):
        self.question = question

        self.text = question.text

        self._time = time.time()
        self.tta = tta

    @property
    def duration(self):
        return time.time() - self._time

    @property
    def time_remaining(self):
        return self.tta - self.duration

    @property
    def json(self):
        return {
            "question": {
                "text": self.question.text,
                "options": self.question.options
            },
            "duration": self.duration,
            "tta": self.time_remaining
        }
