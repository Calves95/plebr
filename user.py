import json


class User:
    def __init__(self, summoner="", id="", region="", sid=""):
        self.summoner = summoner
        self.id = id
        self.region = region
        self.sid = sid

    def __str__(self):
        return json.dumps(self)
