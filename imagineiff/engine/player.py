import os
import uuid
import time

class Player:
    def __str__(self):
        return "%s/%s" % (self.id, self.name)

    def __init__(self, name):
        self.id = str(uuid.UUID(bytes=os.urandom(16)))
        # unused, will be used later for security
        self.auth = str(uuid.UUID(bytes=os.urandom(16)))
        self.name = name

        self.timeout = time.time()

    @property
    def last_ping(self):
        return time.time() - self.timeout
