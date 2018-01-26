"""Base example file for implementing a RESTful game."""
import json
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

    def __init__(self):
        """Initialize the server."""
        pass

    def join_player(self, player_name):
        """Join or kick the player of the game."""
        pass

    def get_handlers(self):
        """Return the different handlers for this game."""
        pass

    def use_handler(self, player_name, handler_name):
        """Use the given handler from the given player."""
        pass

    def get_display(self, player_name):
        """Return the display basing on the player asking."""
        pass

    def is_ready(self, player_name):
        """Tell the server a player is ready."""

if __name__ == "__main__":
    server = Server()
    app.run(host='0.0.0.0')
