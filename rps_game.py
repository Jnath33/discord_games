# Imports
from dislash import ActionRow, Button, ButtonStyle, interactions
import asyncio
import random

# dictionary for the rps
name_to_num = {"r": 3, "p": 2, "s": 1, 1: "ciseaux", 2: "papier", 3: "piere"}
num_to_emote = {1: ":scissors:", 3: ":rock:", 2: ":newspaper:"}
# the rps button
rps_buttons = ActionRow(
    Button(
        style=ButtonStyle.gray,
        label="Pierre",
        custom_id="r",
        emoji="🪨"
    ),
    Button(
        style=ButtonStyle.gray,
        label="Papier",
        custom_id="p",
        emoji="📰"
    ),
    Button(
        style=ButtonStyle.gray,
        label="Ciseaux",
        custom_id="s",
        emoji="✂️"
    )
)


# a simple function for don't nomber have error
def verif_n(n):
    return verif_n(n - 3) if n > 3 else n


# the game classe
class Game:
    async def multi(self, ctx, j_inter, msg):
        # player 1 choosing
        await msg.edit(content=ctx.author.name + " choisis ton choix",
                       components=[rps_buttons])

        def check(inter):
            c_1 = inter.message.id == msg.id
            c_2 = ctx.author == inter.author
            if c_1 and not c_2:
                inter.reply("Vous ne pouvez pas jouer à la place de quelqu'un d'autre", ephemeral=True)
            return inter.message.id == msg.id and ctx.author == inter.author

        p_1_inter = await ctx.wait_for_button_click(check)
        await p_1_inter.reply(content="cequetuveux", type=6)
        # player 2 choosing
        await msg.edit(components=[])
        await msg.edit(content=j_inter.author.name + " choisis ton choix",
                       components=[rps_buttons])

        def check(inter):
            return inter.message.id == msg.id and j_inter.author == inter.author

        p_2_inter = await ctx.wait_for_button_click(check)
        await p_2_inter.reply(content="cequetuveux", type=6)

        # get's id's
        p_1_cho = p_1_inter.clicked_button.custom_id
        p_2_cho = p_2_inter.clicked_button.custom_id

        # roll
        await asyncio.sleep(1)
        await msg.edit(content=num_to_emote[name_to_num[p_1_cho]] + " VS " +
                               num_to_emote[name_to_num[p_2_cho]])
        await asyncio.sleep(1)
        # Select the winner
        if name_to_num[p_1_cho] == name_to_num[p_2_cho]:
            await msg.edit(content=num_to_emote[name_to_num[p_1_cho]] + " VS " +
                                   num_to_emote[name_to_num[p_2_cho]] + " --> ÉGALITÉ")
        elif name_to_num[p_1_cho] == verif_n(name_to_num[p_2_cho] + 1):
            await msg.edit(content=num_to_emote[name_to_num[p_1_cho]] + " VS " +
                                   num_to_emote[name_to_num[p_2_cho]] + " --> VICTOIRE de " +
                                   j_inter.author.name + " J2")
        else:
            await msg.edit(content=num_to_emote[name_to_num[p_1_cho]] + " VS " +
                                   num_to_emote[name_to_num[p_2_cho]] + " --> VICTOIRE de " +
                                   ctx.author.name + " J1")

    async def solo(self, ctx):
        # Send the message with buttons
        msg = await ctx.send(
            "(:rock:) Pierre, (:newspaper:) Papier, (:scissors:) ciseaux choisis le tien",
            components=[rps_buttons]
        )

        # Wait for the player select is signe
        def check(inter):
            return inter.message.id == msg.id and ctx.author == inter.author

        inter = await ctx.wait_for_button_click(check)

        # get cliqued button
        res = inter.clicked_button.custom_id
        # send ready
        await inter.reply(content="cequetuveux", type=6)
        await asyncio.sleep(0.5)
        # delete the message
        tit = 1
        await msg.edit(components=[])
        cho = 1
        # roll
        for i in range(2):
            cho = random.randint(1, 3)
            await msg.edit(content=num_to_emote[cho] + " " + str(tit) + "/2")
            tit += 1
            await asyncio.sleep(0.5)

        # Select the winner
        if cho == name_to_num[res]:
            await msg.edit(content=num_to_emote[cho] + " VS " + num_to_emote[name_to_num[res]] + " --> ÉGALITÉ")
        elif cho == verif_n(name_to_num[res] + 1):
            await msg.edit(content=num_to_emote[cho] + " VS " + num_to_emote[name_to_num[res]] + " --> VICTOIRE")
        else:
            await msg.edit(content=num_to_emote[cho] + " VS " + num_to_emote[name_to_num[res]] + " --> DÉFAITE")
