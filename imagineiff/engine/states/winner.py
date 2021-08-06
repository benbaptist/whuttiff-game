class StateWinner:
    def __str__(self):
        return "winner"

    def __init__(self, winners, players):
        self.winners = winners
        self.players = players

    @property
    def json(self):
        return {
            "winners": [player.json for player in self.winners],
            "players": [player.json for player in self.players]
        }
