# Imports
import json
import sys

import discord
from discord.ext import commands
from dislash import InteractionClient, ActionRow, Button, ButtonStyle

import belote_card_game
import rps_game
import morpion_game

# Init the bot

c_id = 0

bot_settings = json.loads(sys.argv[1])
bot = commands.Bot(command_prefix='!')


async def clear_game_channel():
    for guild in bot.guilds:
        for categories in guild.categories:
            for channel in categories.text_channels:
                if len(channel.name.split("-")) >= 3 and " ".join(channel.name.split("-")[0:2]) == "game card":
                    await channel.delete()
    print("end of clear")


@bot.event
async def on_ready():
    print("Main Bot IS Ready")
    await clear_game_channel()


@bot.command(aliases=["p_4", "p4", "power_4", "power4"])
async def power_four(ctx):
    global c_id
    t_id, c_id = c_id, c_id + 1
    with open("bot1/data/" + str(c_id) + ".json", "x") as f:
        f.write(json.dumps({"cmd": "p4", "c_id": ctx.channel.id,
                            "args": [ctx.message.id]},
                           separators=(',', ':')))


@bot.command(aliases=["morp"])
async def morpion(ctx):
    global c_id
    t_id, c_id = c_id, c_id + 1
    with open("bot1/data/" + str(c_id) + ".json", "x") as f:
        f.write(json.dumps({"cmd": "morpion", "c_id": ctx.channel.id, "args": [ctx.message.id]}, separators=(',', ':')))


@bot.command(aliases=["card", "card_game"])
async def cards(ctx, point: int = 1000):
    global c_id
    t_id, c_id = c_id, c_id + 1
    with open("bot1/data/" + str(c_id) + ".json", "x") as f:
        f.write(json.dumps({"cmd": "card", "c_id": ctx.channel.id, "args": [point]}, separators=(',', ':')))


# create rps cmd with two aliases chifoumi and RPS
@bot.command(aliases=["chifoumi", "RPS"])
async def rps(ctx, *args):
    global c_id
    t_id, c_id = c_id, c_id + 1
    with open("bot1/data/" + str(c_id) + ".json", "x") as f:
        f.write(json.dumps({"cmd": "rps", "c_id": ctx.channel.id, "args": [ctx.author, *args]}, separators=(',', ':')))


bot.run(bot_settings["token"])
