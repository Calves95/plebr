import requests

import utils


class RiotAPI:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_summoner_data(self, region, summonerName):
        URL = "https://" + region + "1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + self.api_key
        response = requests.get(URL)
        return response.json()

    def get_current_game(self, region, ID):
        URL = "https://" + region + "1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + self.api_key
        response = requests.get(URL)
        return response.json()

    def get_ranked_data(self, region, ID):
        URL = "https://" + region + "1.api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + self.api_key
        response = requests.get(URL)
        return response.json()

    def get_champions(self):
        return utils.read_json("Champions.json")


