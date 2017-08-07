import discord
from discord.ext import commands

import db
import utils
from riot_api import RiotAPI
from user import User

config = utils.read_json("config.json")
mDb = db.Memory()

api = RiotAPI(config["riot_api_key"], config["file_location"])

glob = ""
glob2 = ""

Client = discord.Client()
bot_prefix = "!p "
client = commands.Bot(command_prefix=bot_prefix)


@client.event
async def on_ready():
    print("Scanning For LoL Plebs")


# !p commands
@client.command(pass_context=True)
async def commands(ctx):
    buffer = ["```", "!p get_match <region> <summonerName> [used to find entered player's current game]\n",
              "!p register <region> <summonerName> [save your own summoner for quick searching]\n",
              "!p match [used after !p register account has been set, for current match]\n",
              "!p info [gives info on input and extra help]\n", "!p account [check what your username/region"
                                                                " is saved as for quick commands]\n",

              "!p get_stats <region> <summoner> [get  solo ranked stats]\n" "!p stats [used after !p register "
              "account has been set, for solo ranked stats]\n",
              "!p remove [clears your current summoner name and region for quick commands]\n", "```"]

    block = "".join(map(str, buffer))
    await client.say(block)


# !p info
@client.command(pass_context=True)
async def info(ctx):
    buffer = ["```", "1. Do not use spaces for summoner names\n",
              "2. Capitalization does not matter\n",
              "3. type !p commands for instructions on how to use commands""\n",
              "4. Regions: NA/KR/OC/RU/BR/LAN/LAS/JP/EUN/EUW/TR \n",
              "5. Search for Plebs xD\n", "```"]

    block = "".join(map(str, buffer))
    await client.say(block)


# !p register <Region> <SummonerName>
@client.command(pass_context=True)
async def register(ctx, region: str, summoner: str):
    try:
        did = ctx.message.author.id
        d_user = mDb.get_user(did)
        if not d_user:  # user not found
            summ = api.get_summoner_data(region, summoner)
            sid = str(summ['id'])
            await client.say(":inbox_tray: **| Set {}'s Summoner name/region!**".format(ctx.message.author.nick))
            d_user = User(summoner, did, region, sid)
            mDb.upsert_user(d_user)

        else:
            summ = api.get_summoner_data(region, summoner)
            sid = str(summ['id'])
            await client.say(":inbox_tray: **| Set {}'s summoner name/region!**".format(ctx.message.author.nick))
            d_user.summoner = summoner
            d_user.region = region
            d_user.sid = sid
            d_user.id = did
            mDb.upsert_user(d_user)
    except KeyError:
        await client.say(":pencil: | **Make sure region and username is correct when using"
                         " !p register <region> <summoner name> [[!p info for regions]]**")
    except Exception:
        await client.say(":x: **| Use an appropriate region and/or summoner name!**")


# !p remove [removes summoner/region from discord DB]
@client.command(pass_context=True)
async def remove(ctx):
    did = ctx.message.author.id
    mDb.remove_user(did)
    await client.say(":outbox_tray:** | Summoner name and region has been cleared**")


# !p account [Checks for saved username/region]
@client.command(pass_context=True)
async def account(ctx):
    try:
        did = ctx.message.author.id
        name = mDb.get_summoner(did)
        reg = mDb.get_region(did)
        buffer = [":scroll:  **|  __Username:__** ", name, "  **__Region:__** ", reg]
        block = "".join(map(str, buffer))
        await client.say(block)
    except TypeError:
        await client.say(":pencil:  **| Register an account with !p register <region> <summoner name>**")


# !p match [no input, using saved summoner/region]
@client.command(pass_context=True)
async def match(ctx):
    try:
        did = ctx.message.author.id
        summoner_ = mDb.get_summoner(did)
        await client.say(":mag_right: **| Searching for {}'s match**".format(summoner_))
        region_ = mDb.get_region(did)
        find_match(region_, summoner_)
        await client.say(glob)
    except TypeError:
        await client.say(":pencil:  **| Register an account with !p register <region> <summoner name>"
                         " before using this command**")
    except IndexError:
        await client.say(":no_entry_sign:  **| Player Not in Match!**")


# !p get_match <Region> <SummonerName>
@client.command(pass_context=True)
async def get_match(ctx, region: str, summoner: str):
    try:
        await client.say(":mag_right: **| Searching for {}'s match**".format(summoner))
        find_match(region, summoner)
        await client.say(glob)
    except IndexError:
        await client.say(":no_entry_sign:  **| Player Not in match!**")
    except KeyError:
        await client.say(":no_entry_sign:  **| Player Not Recognized!**")
    except Exception:
        await client.say(":pencil: **| Make sure you do !p get_match <Region> <SummonerName> correctly, and"
                         " summoner/region is correct [!p info for regions]**")


# !p get_stats <Region> <SummonerName>
@client.command(pass_context=True)
async def get_stats(ctx, region: str, summoner: str):
    try:
        get_info(region, summoner)
        await client.say(glob2)
    except IndexError:
        await client.say(":no_entry_sign:  **| User Not Ranked**")
    except Exception:
        await client.say(":pencil: **| Make sure you do !p get_stats <Region> <SummonerName> correctly, and"
                         " summoner/region is correct [!p info for regions]**")


# !p stats [no input, using saved summoner/region]
@client.command(pass_context=True)
async def stats(ctx):
    did = ctx.message.author.id
    try:
        summoner_ = mDb.get_summoner(did)
        region_ = mDb.get_region(did)
        get_info(region_, summoner_)
        await client.say(glob2)
    except TypeError:
        await client.say(":pencil: **| Register an account with !p register <region> <summoner name>"
                         " before using this command**")
    except IndexError:
        await client.say(":no_entry_sign:  **| User Not Ranked**")


def get_info(region: str, summoner: str):
    global glob2
    name = api.get_summoner_data(region, summoner)
    sid = name['id']
    sid = str(sid)
    ranked = api.get_ranked_data(region, sid)
    most_played = api.get_most_played(region, sid)
    series = ""

    vet = ""
    fresh = ""
    streak = ""
    league = ranked[0]['leagueName']
    tier = ranked[0]['tier']
    rank = ranked[0]['rank']
    lp = ranked[0]['leaguePoints']
    wins = ranked[0]['wins']
    losses = ranked[0]['losses']
    total = wins + losses
    rate = (1. * wins / total * 100)
    rate_str = str(round((1. * wins / total * 100), 1)) + "%"

    done = []
    if ranked[0]['veteran']:
        vet = done.append(":military_medal:| **Veteran**")
    if ranked[0]['freshBlood']:
        fresh = done.append("**:rosette: | Recently Joined this League**")
    if ranked[0]['hotStreak']:
        streak = done.append(":fire: | **Hot Streak**")


    extras = "     ".join(map(str, done))


    try:
        series = str(ranked[0]['miniSeries']['progress'])
        s = list(series)
        promos = []
        for i in range(len(s)):
            if s[i] == 'W':
                promos.append(":white_check_mark:")
            elif s[i] == 'L':
                promos.append(":negative_squared_cross_mark:")
            else:
                promos.append(":regional_indicator_o:")

        promo = "  ".join(map(str, promos))
        buff = ["\n\n**__Series:__**  ", promo, "\n\n"]
        ser = "".join(map(str, buff))
    except KeyError:
        ser = series

    champ1 = most_played[0]['championId']
    champ2 = most_played[1]['championId']
    champ3 = most_played[2]['championId']

    first = api.get_champion_by_id(champ1)
    sec = api.get_champion_by_id(champ2)
    third = api.get_champion_by_id(champ3)

    champlist = ["**__Favorite Champions__**\n\n", " :one: | ", first, "\n", " :two: | ", sec, "\n", " :three: | ", third]
    top_three = "".join(map(str, champlist))


    if rate >= 75:
        winner = ":crown:"
    elif rate >= 70:
        winner = ":japanese_ogre:"
    elif rate >= 65:
        winner = ":smiling_imp:"
    elif rate >= 60:
        winner = ":astonished:"
    elif rate >= 55:
        winner = ":thumbsup::skin-tone-3:"
    elif rate >= 50:
        winner = ":ok_hand::skin-tone-3: "
    elif rate >= 45:
        winner = ":thinking:"
    else:
        winner = ":eyes:"

    buffer = ["  **(", rate_str, ")**  ", winner]
    block = "".join(map(str, buffer))


    buffer = ["	**__Ranked Solo Stats for:__**  ", summoner, "\n\n", "W/L: ", wins, "/", losses, " ", block, "\n\n"
              "__", league, "__", "\n", "*", tier, " ", rank, "  ", lp, " LP*", ser,
              extras, "\n\n", top_three]

    glob2 = "".join(map(str, buffer))



def find_match(region: str, summoner: str):
    global glob
    name = api.get_summoner_data(region, summoner)
    sid = name['id']
    sid = str(sid)
    print(sid)
    game = api.get_current_game(region, sid)

    try:
        checker = game['participants'][0]['summonerName']
        print(checker)
        game_mode = str(game['gameQueueConfigId'])
        print(game_mode)


        if game_mode == "2":
            mode = ":crossed_swords: | *__Summoner's Rift: Blind Pick__*"
        elif game_mode == "420":
            mode = ":crossed_swords: | *__Summoner's Rift: Solo/Duo Ranked__*"
        elif game_mode == "65":
            mode = ":crossed_swords: | *__Howling Abyss: ARAM__*"
        elif game_mode == "14":
            mode = ":crossed_swords: | *__Summoner's Rift: Draft Pick*"
        elif game_mode == "440":
            mode = ":crossed_swords: | *__Summoner's Rift: Flex Ranked__*"
        elif game_mode == "8":
            mode = ":crossed_swords: | *__Twisted Treeline: Normal*"
        elif game_mode == "8":
            mode = ":crossed_swords: | *__Twisted Treeline: Ranked*"
        else:
            mode = ""


        buffer = [mode, "```"]
        buffer.extend(get_header("BLUE"))
        for x in range(0, 10):

            if x == 5:
                buffer.extend(get_header("RED"))

            name = str(game['participants'][x]['summonerName'])
            IDp = game['participants'][x]['summonerId']
            CID = game['participants'][x]['championId']

            champ = str(api.get_champion_by_id(CID))
            IDp = str(IDp)

            ranked = api.get_ranked_data(region, IDp)
            try:
                tier = ranked[0]['tier']
            except IndexError:
                buffer.append(get_summoner_line(name, champ, "UNRANKED", "N/A", "N/A", "N/A", "N/A"))
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
                winner = "High "
            elif rate >= 55:
                winner = "Above Average"
            elif rate >= 50:
                winner = "Average"
            elif rate >= 45:
                winner = "Below Average"
            else:
                winner = "GLHF"

            buffer.append(get_summoner_line(name, champ, tier, division, LP, rateStr, winner))

        buffer.append("```")
        glob = "\r\n".join(map(str, buffer))
    except KeyError:
        glob = ":no_entry_sign:  **| Player Not in Match!**"
        pass


def get_summoner_line(name, champ, tier, division, LP, rate, winner):
    return "{:<17} {:<16} {:<12} {:<9} {:<4} {:<9} {:<16}".format(name, champ, tier, division, LP, rate, winner)


def get_header(team_color):
    return ['{} {:<4} TEAM {}'.format("=" * 39, team_color, "=" * 39),
            "{:<17} {:<16} {:<12} {:<9} {:<4} {:<9} {:<16}".format(
                "NAME", "CHAMPION", "RANK", "DIVISION", "LP", "Win Rate", "Carry Potential")]


client.run(config["bot_token"])
