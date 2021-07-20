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
            "winning_answer": self.winning_answer,
            "tally": self.tally
        }

    @property
    def tally(self):
        tally = {}

        for player_id in self.question.answers:
            answer = self.question.answers[player_id]

            if answer not in tally:
                tally[answer] = [0, 0] # count, percent

            tally[answer][0] += 1
            tally[answer][1] = float(tally[answer][0]) / len(self.question.answers)

        return tally

    @property
    def winning_answer(self):
        most_id = 0
        most_count = 0

        for answer in self.tally:
            # Compute the option with the most votes
            count = self.tally[answer][0]

            if count > most_count:
                most_id = answer
                most_count = count

        return most_id

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
