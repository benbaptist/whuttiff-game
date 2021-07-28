class Question:
    def __init__(self, question, about):
        self.question = question
        self.about = about

        self.answers = {}

    @property
    def tally(self):
        tally = {}

        for player_id in self.answers:
            answer = self.answers[player_id]

            if answer not in tally:
                tally[answer] = [0, 0] # count, percent

            tally[answer][0] += 1
            tally[answer][1] = float(tally[answer][0]) / len(self.answers)

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
    def winners(self):
        winners = []
        winning_answer = self.winning_answer

        for player_id in self.answers:
            answer = self.answers[player_id]

            if answer == winning_answer:
                winners.append(player_id)

        return winners

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
