import os
import threading
import time

from imagineiff.logmanager import LogManager
from imagineiff.dashboard import Dashboard
from imagineiff.storify import Storify
from imagineiff.config import Config
from imagineiff.engine import Engine

TEMPLATE = {
    "dashboard": {
        "bind": "127.0.0.1",
        "port": 4321
    }
}

class Imagineiff:
    def __init__(self):
        self.log_manager = LogManager()
        self.log = self.log_manager.get_logger("main")

        # Make data folder
        if not os.path.exists("data"):
            os.mkdir("data")

        # Configure configuration
        self.config = Config(path="data/config.json", template=TEMPLATE, log=self.log_manager.get_logger("config"))
        self.config.save()

        # Configure data storage (comment if not needed)
        self.storify = Storify(log=self.log_manager.get_logger("storify"))
        self.db = self.storify.get_db("main")

        # Initialize dashboard (comment if not needed)
        self.dashboard = Dashboard(self, host=self.config["dashboard"]["bind"], port=self.config["dashboard"]["port"])

        # Initilate game engine
        self.engine = Engine(self)

        self.threads = {}
        self.abort = False

    def start(self):
        # Start dashboard (comment if not needed)
        self.threads["dashboard"] = threading.Thread(target=self.dashboard.run, args=())
        self.threads["dashboard"].daemon = True
        self.threads["dashboard"].start()

        try:
            self.run()
        except KeyboardInterrupt:
            self.log.warning("Ctrl+C intercepted")
            self.storify.flush()

    def run(self):
        while not self.abort:
            # Tick
            self.engine.tick()

            # Storify tick
            self.storify.tick()

            time.sleep(1)
