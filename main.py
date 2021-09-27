# Imports
import discord
from discord.ext import commands
from dislash import InteractionClient, ActionRow, Button, ButtonStyle

import belote_card
import belote_card_game
import rps_game
import morpion_game

# Init the bot
bot = commands.Bot(command_prefix="!")
# Init the interaction client in the bot
inter_client = InteractionClient(bot)

join_button = ActionRow(
    Button(
        style=ButtonStyle.green,
        label="Join",
        custom_id="join"
    )
)


async def clear_game_channel():
    for guild in bot.guilds:
        for categories in guild.categories:
            for channel in categories.text_channels:
                if len(channel.name.split("-")) >= 3 and " ".join(channel.name.split("-")[0:2]) == "game card":
                    await channel.delete()
    print("end of clear")


@bot.event
async def on_ready():
    await clear_game_channel()


@bot.event
async def on_message_delete(message):
    print(message.content)


@bot.command(aliases=["morp"])
async def morpion(ctx):
    embed = discord.Embed(title="Waiting", color=0xff8800)

    embed.add_field(name="ㅤ", value=ctx.author.mention + " attend un autre joueur pour jouer au morpion")
    embed.set_footer(text="This game was made by Jnath#5924")

    msg = await ctx.send(embed=embed, components=[join_button])

    def check(inter):
        return inter.message.id == msg.id  # and inter.author != ctx.author

    inter = await ctx.wait_for_button_click(check)
    await inter.reply(content='c', type=6)
    await msg.edit(content="ㅤ", components=[], embed=None)

    await morpion_game.Game(msg, [ctx.author, inter.author]).start()


@bot.command(aliases=["card", "card_game"])
async def cards(ctx, point: int = 1000):
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


# create rps cmd with two aliases chifoumi and RPS
@bot.command(aliases=["chifoumi", "RPS"])
async def rps(ctx, *args):
    # Verify if is multiplayer or solo
    if len(args) > 0 and args[0] in ["m", "multi", "multijoueur", "vs", "versus", "contre"]:
        # send the message
        msg = await ctx.send(ctx.author.name + " a crée une partie appuier sur Join pour rejoindre",
                             components=[join_button])

        # Wait someone click on the button
        def check(inter):
            # is the guy who pressed the button is not the commande sender continu
            return inter.message.id == msg.id and not ctx.author == inter.author

        j_inter = await ctx.wait_for_button_click(check)

        # send message to anoncate who versus who
        await j_inter.reply(content="cequetuveux", type=6)

        # start the multiplayer rps game
        await rps_game.Game().multi(ctx, j_inter, msg)

    else:
        # start the solo rps game
        await rps_game.Game().solo(ctx)


# start the bot
with open("TOKEN", "r") as f:
    bot.run(f.read())
