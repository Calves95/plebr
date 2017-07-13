import json


def read_json(filepath):
    with open(filepath) as f:
        return json.load(f)
