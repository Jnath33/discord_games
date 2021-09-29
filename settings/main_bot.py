import json
import sys
import random

from discord.ext import commands

# Init the command count variable
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
        "pend": 0, # Pendu
        "morp": 1,  # Morpion
        "p4": 2,  # Puissance 4
        "c_name": 3,  # Code name
        "belote": 4,  # Bellote
        "presi": 5,  # Président
        "u_cover": 6,  # Undercover
        "dame": 7,  # Dame
        "chess": 8,  # Échec
        "ksuv": 9  # Ksuv (jeu histoire)
    }


# Set's global usage function
async def game_can_be_start(mode, guild, ctx):
    if len(guild_to_bots[guild.id]) >= mode_to_n_of_bot[mode] or g_settings["main_serv_id"] == guild.id:
        return True
    else:
        await ctx.send("Vous n'avez pas assez de bot !setup")
    return False


def get_r_id(guild):
    return str(random.randint(0, len(guild_to_bots[guild.id])))


def send_command(g_name, ctx, args):
    if await game_can_be_start(g_name, ctx.guild, ctx):
        return
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
    guild_to_bots[guild.id] = 0
    for it in g_settings["settings"]:
        if guild.get_member(int(it["client_id"])) is not None:
            guild_to_bots[guild.id] += it


async def clear_game_channel():
    for guild in bot.guilds:
        for categories in guild.categories:
            for channel in categories.text_channels:
                if len(channel.name.split("-")) >= 3 and " ".join(channel.name.split("-")[0:2]) == "game card":
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
    await clear_game_channel()


@bot.command(aliases=["p_4", "p4", "power_4", "power4"])
async def power_four(ctx):
    send_command("p4", ctx, ctx.message.id)


@bot.command(aliases=["pend"])
async def pendu():
    print("")


@bot.command(aliases=["morp"])
async def morpion(ctx):
    send_command("morp", ctx, [ctx.message.id])


@bot.command(aliases=["bel", "blt"])
async def bellote(ctx, point: int = 1000):
    send_command("belote", ctx, [point])


@bot.command(aliases=["chifoumi", "RPS"])
async def rps(ctx, *args):
    send_command("rps", ctx, [ctx.message.id, *args])


# run bot
bot.run(bot_settings["token"])
