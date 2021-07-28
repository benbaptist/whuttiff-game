import os
import uuid
import random
import time
import copy

from imagineiff.engine.player import Player
from imagineiff.engine.questions import Questions
from imagineiff.engine.questions.question import Question

from imagineiff.engine.states.pregame import StatePregame
from imagineiff.engine.states.statequestion import StateQuestion
from imagineiff.engine.states.results import StateResults

from imagineiff.words import generate_sentence

class Game:
    def __init__(self):
        self.id = str(uuid.UUID(bytes=os.urandom(16)))

        self._questions = copy.deepcopy(Questions)

        self._name = generate_sentence(2)

        self.players = []
        self.removed_players = []
        self.state = StatePregame()
        self.dead = False

        self.time_since_no_players = None

        self.question = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

        self.log.info("Renaming to: %s" % value)

    @property
    def questions(self):
        if len(self._questions) < 1:
            self.log.info("Question pool empty, resetting")
            self._questions = copy.deepcopy(Questions)

        return self._questions

    def start(self):
        assert type(self.state) == StatePregame, "Game already started."
        assert len(self.players) > 1, "Too few players."

        self.log.info("Starting game. Name is %s" % self.name)

        for player in self.players:
            player.reset_game()

        self.pick_question()

    def pick_question(self):
        q = random.choice(self.questions)

        self._questions.remove(q)

        question = Question(
            q,
            random.choice(self.players)
        )

        self.state = StateQuestion(question)

    def skip_results(self):
        assert type(self.state) == StateResults, "Not in results?"

        self.log.info("Skipping results screen")

        self.pick_question()

    def skip_question(self):
        assert type(self.state) == StateQuestion, "Not in question?"

        self.log.info("Skipping question")
        self.pick_question()

    def join(self, name):
        player = Player(
            name,
            len(self.players) == 0 # Makes player admin if no other players
        )
        self.players.append(player)

        return player

    def get_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player

        for player in self.removed_players:
            if player.id == player_id:
                self.log.info("Bringing a dead player back to life!")

                self.players.append(player)
                self.removed_players.remove(player)

                return player

    def tick(self):
        # Check if no players exist, and if so, pause
        if len(self.players) < 1:
            if not self.time_since_no_players:
                self.time_since_no_players = time.time()

            # If it goes ten minutes without any players, consider
            # this game dead and destroy it.
            if time.time() - self.time_since_no_players > 60 * 10:
                self.log.warning("This game needs to be removed.")
                self.dead = True

            return

        # Check player pings, remove inactive players
        for player in self.players:
            if player.last_ping > 60:
                self.log.warning("Removing inactivate player %s" % player)

                self.removed_players.append(player)
                self.players.remove(player)

        if type(self.state) == StateQuestion:
            question = self.state.question

            # Check if all players answered
            if len(self.players) == len(question.answers):
                self.state = StateResults(question)
                self.log.info("Everyone answered.")

        if type(self.state) == StateResults:
            if self.state.duration > 60:
                self.log.info("Time to move on from results..")
                self.skip_results()
