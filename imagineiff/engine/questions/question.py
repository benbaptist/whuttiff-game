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
    def winning_answers(self):
        answers = []

        for answer in self.tally:
            count = self.tally[answer][0]
            answers.append((count, answer))

        answers.sort()
        answers.reverse()

        winning_answers = []

        most_id = 0
        most_count = 0

        for i, answer in enumerate(answers):
            # This is obviously the winning answer. due to the sorting order
            if i == 0:
                most_count, most_id = answer

                winning_answers.append(most_id)
            else:
                count, id = answer

                # print("%s-way tie!" % int(len(winning_answers) + 1))

                if count == most_count:
                    winning_answers.append(id)
                    
        return winning_answers

    @property
    def winners(self):
        winners = []
        winning_answers = self.winning_answers

        for player_id in self.answers:
            answer = self.answers[player_id]

            if answer in winning_answers:
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
