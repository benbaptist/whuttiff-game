from imagineiff.engine.game import Game

class Engine:
    def __init__(self, main):
        self.main = main

        self.log = self.main.log_manager.get_logger("GameEngine")
        self.db = self.main.db

        self.games = []

    def new_game(self):
        game = Game()
        self.games.append(game)

        self.log.info("Creating new game '%s'" % game.id)

        return game

    def get_game(self, id):
        for game in self.games:
            if game.id == id:
                return game

    def tick(self):
        for game in self.games:
            game.tick()
