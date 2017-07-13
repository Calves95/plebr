import discord
from discord.ext import commands

import db
import utils
from riot_api import RiotAPI
from user import User

config = utils.read_json("config.json")
mDb = db.Memory()

api = RiotAPI(config["riot_api_key"])

Client = discord.Client()
bot_prefix = "!p "
client = commands.Bot(command_prefix=bot_prefix)
client.run(config["bot_token"])


@client.event
async def on_ready():
    print("Scanning For LoL Plebs")


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if not message.content.startswith(bot_prefix):
        return

    msg = message.content.replace(bot_prefix, "").split(" ")
    print(msg)
    # user = db.get_user(message.author)
    if msg[0] == "region":
        # set_region(user, region)
        pass
    elif msg[0] == "summonername":
        # set_name(user, summoner)
        pass


def set_region(user, region: str):
    # user.region = msg[0]
    # db.set_user(user)
    pass


def set_name(user, summoner: str):
    # user.summoner = msg[0]
    # db.set_user(user)
    pass


@client.command(pass_context=True)
async def match(ctx):
    get_match(mDb.get_user(ctx.author.id))


@client.command(pass_context=True)
async def match(ctx, summoner: str):
    user = mDb.get_user(ctx.author.id)
    if not user:
        await client.say("Region not set")
        return

    user.summoner = summoner
    get_match(user)


@client.command(pass_context=True)
async def match(ctx, region: str, summoner: str):
    get_match(User(summoner, "", region))


async def get_match(user: User):
    await client.say("Searching match for {}...".format(user.summoner))

    name = api.get_summoner_data(user.region, user.summoner)
    sid = name['id']
    sid = str(sid)
    buffer = ["```"]

    game = api.get_current_game(user.region, sid)

    buffer.extend(get_header("BLUE"))

    for x in range(0, 10):

        if x == 5:
            buffer.extend(get_header("RED"))

        name = game['participants'][x]['summonerName']
        IDp = game['participants'][x]['summonerId']
        cId = game['participants'][x]['championId']
        IDp = str(IDp)

        ranked = api.get_ranked_data(user.region, IDp)
        try:
            tier = ranked[0]['tier']
        except IndexError:
            buffer.append(get_summoner_line(name, "UNRANKED", "N/A", "N/A", "N/A", "N/A"))
            continue

        division = ranked[0]['rank']
        LP = (ranked[0]['leaguePoints'])
        wins = (ranked[0]['wins'])
        lose = (ranked[0]['losses'])
        total = wins + lose
        rate = (1. * wins / total * 100)
        rateStr = str(round((1. * wins / total * 100), 1)) + "%"

        if rate >= 75:
            winner = "SMURF??"
        elif rate >= 70:
            winner = "Extremely High!"
        elif rate >= 65:
            winner = "Very High"
        elif rate >= 60:
            winner = "High"
        elif rate >= 55:
            winner = "Above Average"
        elif rate >= 50:
            winner = "Average"
        elif rate >= 45:
            winner = "Below Average"
        else:
            winner = "GLHF o.o"

        buffer.append(get_summoner_line(name, tier, division, LP, rateStr, winner))

    buffer.append("```")
    strs = "\r\n".join(map(str, buffer))
    print(strs)
    await client.say("\r\n".join(map(str, buffer)))


def get_summoner_line(name, tier, division, LP, rate, winner):
    return "{:<17} {:<12} {:<9} {:<4} {:<9} {:<16}".format(name, tier, division, LP, rate, winner)


def get_header(team_color):
    return ['{} {:<4} TEAM {}'.format("=" * 30, team_color, "=" * 30),
            "{:<17} {:<12} {:<9} {:<4} {:<9} {:<16}".format(
                "NAME", "RANK", "DIVISION", "LP", "Win Rate", "Carry Potential")]
