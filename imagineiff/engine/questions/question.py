class Question:
    def __init__(self, question, about):
        self.question = question
        self.about = about

        self.answers = {}

    @property
    def text(self):
        return \
            self.question["question"].replace("__name__", self.about.name)

    @property
    def options(self):
        return self.question["options"]

    def answer(self, player, answer):
        assert player.id not in self.answers, "Player already answered"

        self.answers[player.id] = answer
