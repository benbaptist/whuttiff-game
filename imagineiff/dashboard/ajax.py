from flask import Flask, redirect, url_for, render_template, \
    request, make_response, Response, Markup, Blueprint, current_app, g

import json
import time

from imagineiff.engine.states.pregame import StatePregame
from imagineiff.engine.states.statequestion import StateQuestion
from imagineiff.engine.states.results import StateResults

blueprint_ajax = Blueprint("ajax", __name__,
        template_folder="templates")

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

        g.game.start()

    elif method == "submit_answer":
        if not g.player:
            return "Nope", 404

        answer = int(request.args["answer"])

        g.game.state.question.answer(g.player, answer)

    elif method == "skip_results":
        g.game.skip_results()

    elif method == "status":
        if not g.game:
            return "Nope", 404

        players = []
        for player in g.game.players:
            players.append({
                "name": player.name,
                "id": player.id,
                "last_ping": player.last_ping
            })

        # if type(g.game.state) == StateQuestion:
        #     question = g.game.state.json

        return json.dumps({
            "id": g.game.id,
            "state": {
                "name": str(g.game.state),
                "payload": g.game.state.json
            },
            "players": players
        })
    else:
        return json.dumps({
            "error": {
                "code": 404,
                "text": "Nope. Not a real method. Get outta here."
            }
        }), 404

    return "Good"
