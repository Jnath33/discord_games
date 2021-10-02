import asyncio

import discord
from dislash import ActionRow, Button, ButtonStyle


async def lobby(ctx, title="Lobby :", description="",
                footer="Veuillez rejoindre la partie 10 secondes après sa création.", color=0x6BDA47,
                label1="Rejoindre", label2="Quitter", timeout=10):
    players = []

    # déclaration de l'embed :
    embed = discord.Embed(title=title, description=description, color=color)
    embed.add_field(name="Joueur :", value="[En attente de joueur]", inline=True)
    embed.set_footer(text=footer)

    # déclaration des boutons :
    lobbybouton = ActionRow(
        Button(
            style=ButtonStyle.green,
            label=label1,
            custom_id="join"
        ),
        Button(
            style=ButtonStyle.red,
            label=label2,
            custom_id="leave"
        )
    )

    # variable msg est l'embed et les boutons stocké
    msg = await ctx.send(embed=embed, components=[lobbybouton])
    # onclick est la variable qui permet d'avoir les event a partir d'un click de bouton
    on_click = msg.create_click_listener(timeout=timeout)

    @on_click.matching_id("join")
    async def on_join(inter):
        liste = ""
        # vérifie si le joueur est dans la partie
        if inter.author in players:
            await inter.reply(content="Vous êtes deja dans la partie", ephemeral=True)
        else:
            # ajoute le joueur dans la liste des joueurs affiché dans l'embed
            players.append(inter.author)
            for row in players:
                liste += "-" + row.mention + "\n"
            # récrer l'embed avec le nouveau joueur
            embed = discord.Embed(title=title, description=description, color=color)
            embed.add_field(name="Joueur :", value=liste, inline=True)
            embed.set_footer(text=footer)
            await msg.edit(embed=embed, components=[lobbybouton])
            await inter.reply(content="t", type=6)

    @on_click.matching_id("leave")
    async def on_leave(inter):
        liste = ""
        # vérifie si le joueur est dans la partie
        if inter.author in players:
            # enleve le joueur dans la liste des joueurs affiché dans l'embed
            del players[players.index(inter.author)]
            for row in players:
                liste += "-" + row.mention + "\n"
            # vérifie si le field des joueurs sera vide après la suppression du joueur
            if liste == "":
                embed = discord.Embed(title=title, description=description, color=color)
                embed.add_field(name="Joueur :", value="[En attente de joueur]", inline=True)
                embed.set_footer(text=footer)
                await msg.edit(embed=embed, components=[lobbybouton])
                await inter.reply(content="t", type=6)
            else:
                embed = discord.Embed(title=title, description=description, color=color)
                embed.add_field(name="Joueur :", value=liste, inline=True)
                embed.set_footer(text=footer)
                await msg.edit(embed=embed, components=[lobbybouton])
                await inter.reply(content="t", type=6)
        else:
            await inter.reply(content="Vous n'êtes pas dans la partie", ephemeral=True)

    await asyncio.sleep(timeout)
    await msg.delete()
    return players
