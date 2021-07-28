from imagineiff.engine.game import Game

class Engine:
    def __init__(self, main):
        self.main = main

        self.log = self.main.log_manager.get_logger("GameEngine")
        self.db = self.main.db

        self.games = []

    def new_game(self):
        game = Game()

        log = self.main.log_manager.get_logger("GameEngine/" + game.id)
        game.log = log
        self.log.info("Creating new game '%s'" % game.id)

        self.games.append(game)

        return game

    def get_game(self, id):
        for game in self.games:
            if game.id == id:
                return game

    def tick(self):
        for game in self.games:

            if game.dead:
                self.games.remove(game)
                continue

            game.tick()
