from flask import Flask, redirect, url_for, render_template, \
    request, make_response, Response, Markup, Blueprint, current_app, g

import json
import time

from imagineiff.engine.states.pregame import StatePregame
from imagineiff.engine.states.statequestion import StateQuestion
from imagineiff.engine.states.results import StateResults

blueprint_ajax = Blueprint("ajax", __name__,
        template_folder="templates")

def safe_chars_check(value):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    allowed_chars += "0123456789_-.,[]{}|!?;:'\" "

    for char in value:
        if char not in allowed_chars:
            raise ValueError("Invalid characters found")

@blueprint_ajax.before_request
def before_request():
    g.app = current_app._main

    g.game = None
    g.player = None

    if "game_id" in request.args and "player_id" in request.args:
        game_id, player_id = request.args["game_id"], request.args["player_id"]

        g.game = g.app.engine.get_game(game_id)
        g.player = g.game.get_player(player_id)

        g.player.timeout = time.time()

@blueprint_ajax.route("/ajax/<path:method>")
def method(method):
    if method == "join":
        player_name = request.args["player_name"]
        game_id = request.args["game_id"]

        try:
            safe_chars_check(player_name)
        except ValueError:
            return "Invalid characters in your username.", 400

        assert len(player_name) < 32 and len(player_name) > 2, "Invalid name length"

        game = g.app.engine.get_game(game_id)
        player = game.join(player_name)

        return json.dumps({
            "player": {
                "name": player.name,
                "id": player.id
            },
            "game": {
                "id": game.id
            }
        })

    elif method == "start":
        if not g.game:
            return "Nope", 404

        if not g.player.is_admin:
            return "Unauthorized", 403

        try:
            g.game.start()
        except AssertionError as e:
            return str(e), 400

    elif method == "submit_answer":
        if not g.player:
            return "Nope", 404

        answer = int(request.args["answer"])

        g.game.state.question.answer(g.player, answer)

    elif method == "skip_question":
        if not g.player.is_admin:
            return "Unauthorized", 403

        g.game.skip_question()

    elif method == "skip_winners":
        if not g.player.is_admin:
            return "Unauthorized", 403

        g.game.skip_winners()

    elif method == "skip_results":
        if not g.player.is_admin:
            return "Unauthorized", 403

        g.game.skip_results()

    elif method == "set-setting":
        if not g.game:
            return "Nope", 404

        if not g.player.is_admin:
            return "Unauthorized", 403

        name = request.args["name"]
        value = request.args["value"]

        print("%s / %s" % (name, value))

        if name == "name":
            try:
                safe_chars_check(value)
            except ValueError:
                return "Bad character", 400

            if len(value) > 32:
                return "Too long", 400

            if len(value) < 4:
                return "Must be at least 4 characters", 400

            g.game.name = value
        elif name == "public":
            try:
                if value == "true":
                    value = True
                else:
                    value = False
            except ValueError:
                return "Invalid value", 400

            g.game.public = value
        elif name == "max-score":
            try:
                value = int(value)
            except ValueError:
                return "Invalid value", 400

            g.game.max_score = value
        elif name == "max-players":
            try:
                value = int(value)
            except ValueError:
                return "Invalid value", 400

            if value > 50:
                return "Too many players", 400
            elif value < 3:
                return "Too few players", 400

            g.game.max_players = value

    elif method == "status":
        if not g.game:
            return "Nope", 404

        players = []
        for player in g.game.players:
            players.append({
                "name": player.name,
                "id": player.id,
                "last_ping": player.last_ping,
                "is_admin": player.is_admin
            })

        scoreboard = {}

        for player in g.game.players:
            if player.score == None:
                return

            scoreboard[player.id] = {
                "score": player.score,
                "percent": player.score_percent,
                "leading": player.leading
            }

        return json.dumps({
            "id": g.game.id,
            "state": {
                "name": str(g.game.state),
                "payload": g.game.state.json
            },
            "game_name": g.game.name,
            "players": players,
            "is_admin": g.player.is_admin,
            "scoreboard": scoreboard
        })
    else:
        return json.dumps({
            "error": {
                "code": 404,
                "text": "Nope. Not a real method. Get outta here."
            }
        }), 404

    return "Good"
