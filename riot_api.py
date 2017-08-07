import requests

import json


class RiotAPI:


    def __init__(self, api_key, file_location):
        self.api_key = api_key
        self.file_location = file_location

    def get_summoner_data(self, region, summonerName):
        URL = "https://" + region + "1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + self.api_key
        if region == "kr":
            URL = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + self.api_key
        if region == "ru":
            URL = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + self.api_key
        if region == "las":
            URL = "https://la2.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + self.api_key
        if region == "lan":
            URL = "https://la1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + summonerName + "?api_key=" + self.api_key

        response = requests.get(URL)
        return response.json()


    def get_current_game(self, region, ID):
        URL = "https://" + region + "1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "kr":
            URL = "https://" + region + ".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "ru":
            URL = "https://" + region + ".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "las":
            URL = "https://la2.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "lan":
            URL = "https://la1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + ID + "?api_key=" + self.api_key

        response = requests.get(URL)
        return response.json()


    def get_ranked_data(self, region, ID):
        URL = "https://" + region + "1.api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "kr":
            URL = "https://" + region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "ru":
            URL = "https://" + region + ".api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "las":
            URL = "https://la2.api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "lan":
            URL = "https://la1.api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + self.api_key

        response = requests.get(URL)
        return response.json()

    def get_most_played(self, region, ID):

        URL = "https://" + region + "1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "kr":
            URL = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "ru":
            URL = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "las":
            URL = "https://la2.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/" + ID + "?api_key=" + self.api_key
        if region == "lan":
            URL = "https://la1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/" + ID + "?api_key=" + self.api_key

        response = requests.get(URL)
        return response.json()

    def get_champion_by_id(self, CID):
        f = open(self.file_location, "r")
        s = f.read()
        champs = json.loads(s)

        for key, value in champs['data'].items():
            if champs['data'][key]['id'] == CID:
                return champs['data'][key]['name']

