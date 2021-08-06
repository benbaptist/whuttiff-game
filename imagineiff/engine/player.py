import os
import uuid
import time

class Player:
    def __str__(self):
        return "%s/%s" % (self.id, self.name)

    @property
    def json(self):
        return {
            "name": self.name,
            "id": self.id,
            "score": {
                "percent": self.score_percent,
                "points": self.score
            },
            "last_ping": self.last_ping,
            "is_admin": self.is_admin
        }

    def __init__(self, name, is_admin):
        self.id = str(uuid.UUID(bytes=os.urandom(16)))
        # unused, will be used later for security
        self.auth = str(uuid.UUID(bytes=os.urandom(16)))
        self.name = name

        self.is_admin = is_admin

        self.timeout = time.time()

        self.score = 0
        # Unimplemented, will be used for checking if players are inactive
        self.rounds_since_answering = 0

        self.score_percent = None
        self.leading = False

    def reset_game(self):
        self.score = 0

    @property
    def last_ping(self):
        return time.time() - self.timeout
