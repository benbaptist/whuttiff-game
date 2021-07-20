class StateQuestion:
    def __str__(self):
        return "question"

    def __init__(self, question):
        self.question = question

        self.text = question.text

    @property
    def json(self):
        return {
            "question": {
                "text": self.question.text,
                "options": self.question.options
            }
        }
