import socket
import docker
import tarfile
import json
import os
from flask import Flask, request
from flask_restful import Resource, Api
from contextlib import closing

app = Flask(__name__)
api = Api(app)

client = docker.from_env()

class Matchmaker(Resource):
    def get(self, game_name):
        if server.has_game(game_name) is not None:
            return server.has_game(game_name)
        return server.create_matchmaking(game_name)


class Gamelist(Resource):
    def get(self):
        return json.dumps(server.games)


class Matchpinger(Resource):
    def get(self, match_id):
        return json.dumps(server.match_making[match_id])


class Matchjoiner(Resource):
    def get(self, match_id, p_name):
        if len(server.match_making[match_id]["players"]) < 2:
            server.match_making[match_id]["players"].append(p_name)
            if len(server.match_making[match_id]["players"]) == 2:
                server.match_making[match_id]["ready"] = True
                server.match_making[match_id]["port"] = server.create_instance(server.match_making[match_id]["game"])
            return json.dumps(server.match_making[match_id])
        else:
            return "0"


api.add_resource(Gamelist, '/games')
api.add_resource(Matchmaker, '/getmatch/<string:game_name>')
api.add_resource(Matchpinger, '/match/<int:match_id>/status')
api.add_resource(Matchjoiner, '/match/<int:match_id>/join/<string:p_name>')

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:") as tar:
        tar.add(source_dir, arcname=os.path.sep)


class Server(object):

    def __init__(self):
        self.match_making = []
        self.games = []
        self.cont = []
        with open("games_list.txt", 'r') as r_file:
            game_list = r_file.read()
        for i in game_list.split('\n'):
            if len(i):
                self.games.append(i)
        try:
            image = client.images.get("run_game")
        except docker.errors.ImageNotFound:
            image = client.images.build(path=".",
                                        tag="run_game",
                                        pull=True,
                                        dockerfile="Dockerfile")
        except docker.errors.APIError:
            pass

    def create_instance(self, game_name):
        new_port = find_free_port()
        container = client.containers.create("run_game",
                                             command="python server.py",
                                             auto_remove=True,
                                             name=(game_name + str(len(self.cont))),
                                             working_dir="/home/game",
                                             ports={'5000/tcp': new_port})
        make_tarfile(game_name + '.tar', game_name)
        with open(game_name + '.tar', 'r') as tar:
            container.put_archive("/home/game", tar.read())
        self.cont.append(container)
        self.cont[-1].start()
        return new_port

    def has_game(self, game_name):
        for i in range(len(self.match_making)):
            if self.match_making[i]["game"] == game_name and self.match_making[i]["port"] == 0:
                return i
        return None

    def create_matchmaking(self, game_name):
        self.match_making.append({
            "players": [],
            "game": game_name,
            "ready": False,
            "port": 0
        })
        return len(self.match_making) - 1
        
if __name__ == "__main__":
    try:
        server = Server()
        app.run(host='0.0.0.0')
    finally:
        for i in server.cont:
            i.stop()