from flask import g
from flask_socketio import Namespace, send, emit, join_room, leave_room

import time

class Events(Namespace):
    def __init__(self, socketio):
        self.socketio = socketio

    def on_join(self, game_id):
        print("Game id", game_id)
        return
