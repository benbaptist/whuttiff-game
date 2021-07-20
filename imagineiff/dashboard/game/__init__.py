from flask import Flask, redirect, url_for, render_template, \
    request, make_response, Response, Markup, Blueprint, current_app, g

blueprint_game = Blueprint("game", __name__,
        template_folder="templates")

@blueprint_game.before_request
def before_request():
    g.app = current_app._main

@blueprint_game.route("/create_game")
def create_game():
    game = g.app.engine.new_game()

    return redirect("/game/%s" % game.id)

@blueprint_game.route("/game/<path:game_id>")
def game_session(game_id):
    game = g.app.engine.get_game(game_id)

    if not game:
        return redirect("/")

    return render_template("game.html", game=game)
