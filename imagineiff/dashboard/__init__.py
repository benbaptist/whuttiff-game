from flask import Flask, g, redirect, url_for, render_template, request, make_response, Response, Markup
from flask_socketio import SocketIO, send, emit, join_room, leave_room

import os
import signal
import time
import random
import json
import traceback
import datetime
import requests

from imagineiff.dashboard.game import blueprint_game
from imagineiff.dashboard.ajax import blueprint_ajax

class Dashboard:
    def __init__(self, main, host="127.0.0.1", port=4321, portDebug=5432, debugMode=False):
        self.main = main
        self.host = host
        self.port = port
        self.portDebug = portDebug
        self.debugMode = debugMode

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = ""
        self.app.config['MINIFY_PAGE'] = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.app.jinja_env.add_extension('jinja2.ext.loopcontrols')
        self.app._main = main

        self.socketio = SocketIO(self.app)
        self.register_blueprints()

    def generateKey(self, length):
        a = None

        while not a:
            a = ""
            symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-!@#$%^&*()"
            for i in range(length):
                a += random.choice(symbols)
        return a

    def add_decorators(self):
        # Pages
        @self.app.route("/")
        def index():
            return render_template("index.html", games=self.main.engine.games)

        # Custom filters
        @self.app.template_filter()
        def dt(ts):
            date = datetime.datetime.utcfromtimestamp(ts)
            return date.strftime('%Y-%m-%d @ %H:%M:%S')

        # Error handling
        @self.app.errorhandler(AssertionError)
        def all_exception_handler(error):
            try:
                msg = str(error)

                if request.headers.getlist("X-Forwarded-For"):
                   ip = request.headers.getlist("X-Forwarded-For")[0]
                else:
                   ip = request.remote_addr

                errorInfo = {
                    "errorMsg": msg,
                    "time": time.time(),
                    "headers": str(request.headers),
                    "ip": ip
                }

                print("ERROR: %s" % str(errorInfo))

                return "<h1>Internal Server Error</h1>", 500
            except:
                traceback.print_exc()
                return "<h1>Something went VERY south. Contact an administrator, please.</h1>", 500
    def register_blueprints(self):
        self.app.register_blueprint(blueprint_game)
        self.app.register_blueprint(blueprint_ajax)

    def run(self):
        self.add_decorators()
        if self.debugMode:
            self.socketio.run(self.app, host=self.host, port=self.portDebug, debug=True, use_reloader=False)
        else:
            self.socketio.run(self.app, host=self.host, port=self.port, debug=False, use_reloader=False)
