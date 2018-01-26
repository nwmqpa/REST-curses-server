"""Server file for implementing a RESTful sokoban."""
import json
from map_code import Map
from flask import Flask, request
from flask_restful import Resource, Api
from contextlib import closing

app = Flask(__name__)
api = Api(app)


class ToDisplay(Resource):
    """Class responsible to send the display basing on player."""

    def get(self, player_name):
        """GET protocol of RESTful API."""
        return server.get_display(player_name)


class GetHandlers(Resource):
    """Class responsible of sending the differents handlers."""

    def get(self):
        """GET protocol of RESTful API."""
        return server.get_handlers()


class UseHandlers(Resource):
    """Class responsible of the use of different handlers."""

    def get(self, player_name, handle):
        """GET protocol of RESTful API."""
        return server.use_handler(player_name, handle)


class JoinGame(Resource):
    """Class responsible for the joining of the game."""

    def get(self, player_name):
        """GET protocol of RESTful API."""
        return server.join_player(player_name)


class ReadyPlayer(Resource):
    """Class responsible of telling the server a player is ready."""

    def get(self, player_name):
        """GET protocol of RESTful API."""
        return server.is_ready(player_name)

api.add_resource(ReadyPlayer, '/ready/<string:player_name>')
api.add_resource(ToDisplay, '/display/<string:player_name>')
api.add_resource(GetHandlers, '/handlers')
api.add_resource(UseHandlers, '/handlers/<string:player_name>/<string:handle>')
api.add_resource(JoinGame, '/join/<string:player_name>')


class Server(object):
    """Game server object. Game should essentially managed here."""

    handlers = {
        "move_left": "Move player left.",
        "move_right": "Move player right.",
        "move_up": "Move player up.",
        "move_down": "Move player down."
    }

    def __init__(self):
        """Initialize the server."""
        self.players = []
        self.ready = []
        self.map = Map("map.txt")

    def join_player(self, player_name):
        """Join or kick the player of the game."""
        if len(self.players) < 2 and player_name not in self.players:
            self.players.append(player_name)
            return 1
        else:
            return 0

    def get_handlers(self):
        """Return the different handlers for this game."""
        return json.dumps(self.handlers)

    def use_handler(self, player_name, handler_name):
        """Use the given handler from the given player."""
        if len(self.ready) == 2 and player_name in self.ready:
            x = 0
            y = 0
            if self.ready[0] == player_name:
                x, y = self.map.get_player_1()
            else:
                x, y = self.map.get_player_2()    
            if handler_name == "move_left":
                self.map.move_at(x, y, -1, 0)
            elif handler_name == "move_right":
                self.map.move_at(x, y, 1, 0)
            elif handler_name == "move_up":
                self.map.move_at(x, y, 0, -1)
            elif handler_name == "move_down":
                self.map.move_at(x, y, 0, 1)
        else:
            return "player_not_found"

    def get_display(self, player_name):
        """Returns the display basing on the player asking."""
        if len(self.ready) == 2 and player_name in self.ready:
            return self.map.get_display()
        return "Waiting other players..."

    def is_ready(self, player_name):
        """Tell the server a player is ready."""
        if player_name not in self.players:
            return 0
        if player_name not in self.ready:
            self.ready.append(player_name)
            return 1

if __name__ == "__main__":
    server = Server()
    app.run(host='0.0.0.0')
