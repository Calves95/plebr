import json


class User:
    def __init__(self, summoner="", id="", region="", sid=""):
        self.summoner = summoner
        self.id = id
        self.sid = sid
        self.region = region

    def __str__(self):
        return json.dumps(self)
