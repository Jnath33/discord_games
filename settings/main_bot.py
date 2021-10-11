import json
import sys
import random

from discord.ext import commands

# Init the command count variable
import color_z.colorz as cz

current_cmd_count = 0

# init the variable neded to calculate the bot repartition
bots_member_serv = {}
total_bots_member_serv = 0
guild_to_bots = {}

# loads the setings and launch the bot
with open("settings/settings.json", "r") as f:
    g_settings = json.load(f)

bot_settings = json.loads(sys.argv[1])
id_max = int(sys.argv[2])  # The maximum id

bot = commands.Bot(command_prefix='!')

# The list of game with the number of bot in the server needed to run the game
mode_to_n_of_bot = \
    {
        "rps": 0,  # Pierre feuille ciseaux,
        "pendu": 0,  # Pendu
        "morp": 1,  # Morpion
        "p4": 2,  # Puissance 4
        "c_name": 3,  # Code name
        "colorz": 3,  # ColorZ
        "belote": 4,  # Bellote
        "presi": 5,  # Président
        "u_cover": 6,  # Undercover
        "dame": 7,  # Dame
        "chess": 8,  # Échec
        "ksuv": 9  # Ksuv (jeu histoire)
    }


# Set's global usage function
async def game_can_be_start(mode, guild, ctx):
    if len(guild_to_bots[guild.id]) >= mode_to_n_of_bot[mode] or guild.id in g_settings["main_serv_id"]:
        return True
    else:
        await ctx.send("Vous n'avez pas assez de bot !setup")
    return False


def get_r_id(guild):
    return str(random.randint(0, len(guild_to_bots[guild.id])))


async def send_command(g_name, ctx, args):
    if await game_can_be_start(g_name, ctx.guild, ctx):
        global current_cmd_count
        t_id, current_cmd_count = current_cmd_count, current_cmd_count + 1
        with open("bot" + get_r_id(ctx.guild) + "/" +
                  "data/" +
                  str(current_cmd_count) + "-cmd.json", "x") as f:
            f.write(json.dumps({"cmd": g_name, "c_id": ctx.channel.id,
                                "args": args},
                               separators=(',', ':')))


def register_guild(guild):
    global guild_to_bots
    guild_to_bots[guild.id] = []
    for it in g_settings["settings"]:
        if guild.get_member(int(it["client_id"])) is not None:
            guild_to_bots[guild.id].append(guild.get_member(int(it["client_id"])))


async def clear_game_channel():
    for guild in bot.guilds:
        for categories in guild.categories:
            for channel in categories.text_channels:
                info = channel.name.split("-")
                if len(info) >= 3 and " ".join(info[0:2]) == "game card":
                    await channel.delete()
                if len(info) == 3 and info[1] == "pendu_game":
                    await channel.delete()
    print("end of clear")


# Set's the variable needed to calculate the bot repartition
for i in range(id_max + 1):
    bots_member_serv[i] = 0

for s in bot.guilds:
    for i in range(id_max + 1):
        bots_member_serv[i] += s.member_count


# bot's function
@bot.event
async def on_ready():
    print("Main Bot IS Ready")
    for guild in bot.guilds:
        register_guild(guild)
    await clear_game_channel()


@bot.command(aliases=["cz", "colorZ", "color_z"])
async def colorz(ctx):
    await send_command("colorz", ctx, [ctx.message.id])


@bot.command(aliases=["p_4", "p4", "power_4", "power4"])
async def power_four(ctx):
    await send_command("p4", ctx, [ctx.message.id])


@bot.command(aliases=['leaderboard', 'sb', "scoreboard"])
async def lb(ctx, *args):
    await cz.lb(ctx.channel, ctx.author, *args)


@bot.command(aliases=["pend"])
async def pendu(ctx):
    await send_command("pendu", ctx, [])


@bot.command(aliases=["morp"])
async def morpion(ctx):
    await send_command("morp", ctx, [ctx.message.id])


@bot.command(aliases=["bel", "blt"])
async def bellote(ctx, point: int = 1000):
    await send_command("belote", ctx, [point])


@bot.command(aliases=["chifoumi", "RPS"])
async def rps(ctx, *args):
    await send_command("rps", ctx, [ctx.message.id, *args])


@bot.command(aliases=["under"])
async def undercover(ctx):
    await send_command("undercover", ctx, [])

# run bot
bot.run(bot_settings["token"])
