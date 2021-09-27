import asyncio

import discord
import sys
import json
from os import walk, remove
from dislash import InteractionClient, ActionRow, Button, ButtonStyle

import belote_card_game
import morpion_game
import rps_game

bot_settings = json.loads(sys.argv[1])

bot = discord.Client()

# Init the interaction client in the bot

inter_client = InteractionClient(bot)

join_button = ActionRow(
    Button(
        style=ButtonStyle.green,
        label="Join",
        custom_id="join"
    )
)

commands = {}


def command(func):
    commands[func.__name__] = func


@bot.event
async def on_ready():
    print("Bot " + bot_settings["id"])
    bot.loop.create_task(update())


async def update():
    while True:
        filenames = next(walk("bot" + bot_settings["id"] + "/data"), (None, None, []))[2]
        for file in filenames:
            with open("bot" + bot_settings["id"] + "/data/" + file, "r") as f:
                data = json.load(f)
                if data["cmd"] in commands:
                    bot.loop.create_task(commands[data["cmd"]](data["c_id"], *data["args"]))
            remove("bot" + bot_settings["id"] + "/data/" + file)
        await asyncio.sleep(.5)


@command
async def morpion(c_id, author_id):
    ctx = bot.get_channel(c_id)
    author = bot.get_user(author_id)
    embed = discord.Embed(title="Waiting", color=0xff8800)

    embed.add_field(name="ㅤ", value=author.mention + " attend un autre joueur pour jouer au morpion")
    embed.set_footer(text="This game was made by Jnath#5924")

    msg = await ctx.send(embed=embed, components=[join_button])

    def check(inter):
        return inter.message.id == msg.id  # and inter.author != ctx.author

    inter = await ctx.wait_for_button_click(check)
    await inter.reply(content='c', type=6)
    await msg.edit(content="ㅤ", components=[], embed=None)

    await morpion_game.Game(msg, [author, inter.author]).start()


@command
async def card(c_id, point):
    ctx = bot.get_channel(c_id)
    # Create lobby and wait the four player join
    # after create the game and start it
    joins_button = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="Rejoindre Nord",
            custom_id="n",
            emoji="🇳"
        ),
        Button(
            style=ButtonStyle.green,
            label="Rejoindre Sud",
            custom_id="s",
            emoji="🇸"
        ),
        Button(
            style=ButtonStyle.green,
            label="Rejoindre Est",
            custom_id="e",
            emoji="🇪"
        ),
        Button(
            style=ButtonStyle.green,
            label="Rejoindre Ouest",
            custom_id="o",
            emoji="🇴"
        )
    )

    button_to_n = {"n": 0, "s": 1, "e": 2, "o": 3}
    pressed_buttons = []
    games_player = {}
    game_player_inter = {}

    # create waiting embed
    embed = discord.Embed(color=0xff8800)
    embed.add_field(name="Belote", value="ㅤ" +
                                         "\nJoueur Nord : " + (
                                             games_player["n"].mention if "n" in games_player else "[Waiting]") +
                                         "\nJoueur Sud : " + (
                                             games_player["s"].mention if "s" in games_player else "[Waiting]") +
                                         "\nJoueur Est : " + (
                                             games_player["e"].mention if "e" in games_player else "[Waiting]") +
                                         "\nJoueur Ouest : " + (
                                             games_player["o"].mention if "o" in games_player else "[Waiting]")
                    )
    embed.set_footer(text="This game was made by Jnath#5924")
    # send embed
    j_msg = await ctx.send(embed=embed,
                           components=[joins_button])

    # wait player join
    for i in range(4):
        def check(inter):
            c_1 = inter.message.id == j_msg.id
            if c_1:
                n_to_remove = 0
                button_int_id = button_to_n[inter.clicked_button.custom_id]
                if button_int_id in pressed_buttons:
                    return False
                for pressed_button in pressed_buttons:
                    if button_int_id > pressed_button:
                        n_to_remove += 1
                pressed_buttons.append(button_int_id)
                del joins_button.buttons[button_int_id - n_to_remove]
                return True
            return False

        j_inter = await ctx.wait_for_button_click(check)

        await j_inter.reply(content="cequetuveux", type=6)

        games_player[j_inter.clicked_button.custom_id] = j_inter.author
        game_player_inter[j_inter.clicked_button.custom_id] = j_inter

        embed.set_field_at(
            index=0,
            value="ㅤ" +
                  "\nJoueur Nord : " + (
                      games_player["n"].mention if "n" in games_player else "[Waiting]") +
                  "\nJoueur Sud : " + (
                      games_player["s"].mention if "s" in games_player else "[Waiting]") +
                  "\nJoueur Est : " + (
                      games_player["e"].mention if "e" in games_player else "[Waiting]") +
                  "\nJoueur Ouest : " + (
                      games_player["o"].mention if "o" in games_player else "[Waiting]"),
            name="Belote"
        )
        if len(joins_button.buttons) > 0:
            await j_msg.edit(components=[joins_button], embed=embed)
        else:
            await j_msg.edit(embed=embed)

    # start the game
    game = belote_card_game.Game(games_player, game_player_inter, ctx, j_msg, point)
    if game.can_start:
        await game.end_init()
        await j_msg.edit(components=[], content="La game démarre regarde le channel sur le coté")
        await game.start()
    else:
        await j_msg.edit(components=[], content="Une érreur est survenue vous ne pouver pas démarer de partie")


@command
async def rps(c_id, author_id, *args):
    ctx = bot.get_channel(c_id)
    author = bot.get_user(author_id)
    # Verify if is multiplayer or solo
    if len(args) > 0 and args[0] in ["m", "multi", "multijoueur", "vs", "versus", "contre"]:
        # send the message
        msg = await ctx.send(author.name + " a crée une partie appuier sur Join pour rejoindre",
                             components=[join_button])

        # Wait someone click on the button
        def check(inter):
            # is the guy who pressed the button is not the commande sender continu
            return inter.message.id == msg.id and not author == inter.author

        j_inter = await msg.wait_for_button_click(check)

        # send message to anoncate who versus who
        await j_inter.reply(content="cequetuveux", type=6)

        # start the multiplayer rps game
        await rps_game.Game().multi(j_inter, msg, author)

    else:
        # start the solo rps game
        await rps_game.Game().solo(ctx, author)


bot.run(bot_settings["token"])
