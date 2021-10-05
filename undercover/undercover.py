import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import random
import pandas
import uuid
from dislash import *

mots = pandas.read_csv(r"Undercover.csv")
jeux = {}


async def start(channel, guild):
    global mots
    global jeux
    lobbybouton = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="Rejoindre la partie",
            custom_id="join"
        ),
        Button(
            style=ButtonStyle.red,
            label="Quitter la partie",
            custom_id="leave"
        )
    )
    embed = discord.Embed(
        title="Undercover", description="Etat de la partie : **En attente de joueur**", color=0xeeff00)
    embed.add_field(
        name="Joueurs", value="[En attente de joueur]", inline=True)
    embed.set_footer(text="Vous avez 60 secondes pour rejoindre la partie")
    msg = await channel.send(embed=embed, components=[lobbybouton])
    on_click = msg.create_click_listener(timeout=15)

    @on_click.matching_id("join")
    async def on_join(inter):
        global jeux
        if inter.author in jeux.keys():
            await inter.reply(content="Vous êtes deja dans la partie", ephemeral=True)
        else:
            jeux[inter.author] = ["Civil", "En vie", "motbase", "mot1", "mot2", "vote"]
            joueurs = ""
            for key in jeux:
                joueurs += key.mention + "\n"
            embed = discord.Embed(
                title="Undercover", description="Etat de la partie : **En attente de joueur**", color=0xeeff00)
            embed.add_field(name="Joueurs", value=joueurs, inline=True)
            embed.set_footer(
                text="Vous avez 60 secondes pour rejoindre la partie")
            await msg.edit(embed=embed, components=[lobbybouton])
            await inter.reply(content="t", type=6)

    @on_click.matching_id("leave")
    async def on_leave(inter):
        global jeux
        if inter.author in jeux.keys():
            jeux.pop(inter.author, None)
            joueurs = ""
            for key in jeux:
                joueurs += key.mention + "\n"
            if joueurs == "":
                embed = discord.Embed(
                    title="Undercover", description="Etat de la partie : **En attente de joueur**", color=0xeeff00)
                embed.add_field(
                    name="Joueurs", value="[En attente de joueur]", inline=True)
                embed.set_footer(
                    text="Vous avez 60 secondes pour rejoindre la partie")
                await msg.edit(embed=embed, components=[lobbybouton])
                await inter.reply(content="t", type=6)
            else:
                embed = discord.Embed(
                    title="Undercover", description="Etat de la partie : **En attente de joueur**", color=0xeeff00)
                embed.add_field(name="Joueurs", value=joueurs, inline=True)
                embed.set_footer(
                    text="Vous avez 60 secondes pour rejoindre la partie")
                await msg.edit(embed=embed, components=[lobbybouton])
                await inter.reply(content="t", type=6)
        else:
            await inter.reply(content="Vous n'êtes pas dans la partie", ephemeral=True)

    @on_click.timeout
    async def on_timeout():
        global jeux
        joueurs = ""
        joueurs2 = ""
        for key in jeux:
            joueurs += key.mention + "\n"
            joueurs2 += key.mention + "\n"
        embed = discord.Embed(
            title="Undercover", description="Etat de la partie : **Chargement de la partie...**", color=0xffa200)
        embed.add_field(name="Joueurs", value=joueurs, inline=True)
        embed.set_footer(text="Le temps d'attente est terminé")
        await msg.edit(embed=embed, components=[])
        await asyncio.sleep(1)
        if len(jeux.keys()) >= 2:
            category = discord.utils.get(
                guild.categories, id=880844727333822485)
            chan = await guild.create_text_channel("UnderCover" + uuid.uuid4().hex, category=category)
            embed = discord.Embed(
                title="Undercover", description="Etat de la partie : **Partie créer !**\n" + chan.mention,
                color=0x37ff00)
            embed.set_footer(text="Le temps d'attente est terminé")
            await msg.edit(embed=embed, components=[])
            joueurs = "||"
            for key in jeux:
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.read_messages = True
                await chan.set_permissions(key, overwrite=overwrite)
                joueurs += key.mention
            joueurs += "||"
            supr = await chan.send(content=joueurs)
            await supr.delete()

            nbchoix = random.randint(0, len(mots["mot1"]) - 1)
            for value in jeux.values():
                value[2] = mots["mot1"][nbchoix]
            joueurslist = []
            for key in jeux.keys():
                joueurslist.append(key)
            undercover = random.randint(0, len(joueurslist) - 1)
            jeux[joueurslist[undercover]][2] = mots["mot2"][nbchoix]
            jeux[joueurslist[undercover]][0] = "Undercover"

            revealbouton = ActionRow(
                Button(
                    style=ButtonStyle.green,
                    label="Révélation",
                    custom_id="reveal"
                )
            )
            embed = discord.Embed(
                title="Undercover", description="Merci d'appuyer sur le bouton pour révéler votre mot !",
                color=0xfbff00)
            embed.add_field(name="Joueurs", value=joueurs2, inline=True)
            embed.set_footer(text="Vous avez 20 secondes")
            msg2 = await chan.send(embed=embed, components=[revealbouton])
            on_click2 = msg2.create_click_listener(timeout=20)

            @on_click2.matching_id("reveal")
            async def on_reveal(inter):
                if inter.author in jeux.keys():
                    await inter.reply(content="Ton mot est : " + jeux[inter.author][2], ephemeral=True)
                else:
                    await inter.reply(content="Tu n'est pas dans la partie", ephemeral=True)

            @on_click2.timeout
            async def on_timeout():
                embed = discord.Embed(
                    title="Undercover", description="Début de la partie !", color=0x37ff00)
                embed.add_field(name="Joueurs", value=joueurs2, inline=True)
                await msg2.edit(embed=embed, components=[])

                def check(m: discord.Message):
                    return m.author.id == m.author.id and m.channel.id == chan.id

                for nbfais in range(3, 5):
                    for key in jeux.keys():
                        await chan.send(
                            content=key.mention + " C'est a votre tour de proposer un mot !\nVous avez 30 secondes")
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = True
                        overwrite.read_messages = True
                        await chan.set_permissions(key, overwrite=overwrite)
                        try:
                            msgkey = await bot.wait_for(event='message', check=check, timeout=30.0)
                        except asyncio.TimeoutError:
                            overwrite = discord.PermissionOverwrite()
                            overwrite.send_messages = False
                            overwrite.read_messages = True
                            await chan.set_permissions(key, overwrite=overwrite)
                            jeux[key][nbfais] = "Non renseigné"
                            await chan.send(
                                content=key.mention + " Les 30 secondes sont terminé et vous n'avez rien proposé, votre mot sera donc : Non renseigné")
                        else:
                            overwrite = discord.PermissionOverwrite()
                            overwrite.send_messages = False
                            overwrite.read_messages = True
                            await chan.set_permissions(key, overwrite=overwrite)
                            jeux[msgkey.author][nbfais] = msgkey.content
                motsjoueurrecap = ""
                joueurslist = []
                boutonvote = ActionRow()
                embed = discord.Embed(title="Récapitulatif",
                                      description="Voila un petit récapitulatif des mots de chaque joueur")
                for key in jeux.keys():
                    motsjoueurrecap += "-" + jeux[key][3] + "\n"
                    motsjoueurrecap += "-" + jeux[key][4] + "\n"
                    embed.add_field(name=key.display_name, value=motsjoueurrecap, inline=True)
                    motsjoueurrecap = ""
                    boutonvote.add_button(style=ButtonStyle.green, label=key.display_name, custom_id=key.id)
                    joueurslist.append(key)
                await chan.send(embed=embed)
                await asyncio.sleep(3)
                embed = discord.Embed(title="Vote",
                                      description="C'est l'heure de passer au vote !\nCliquez sur le bouton correspondant a la personne pour laquelle vous voulez voter :)\nRappel : Vous pouvez changer de vote jusqu'au dernier moment.")
                embed.set_footer(text="Vous avez 60 secondes")
                msg3 = await chan.send(embed=embed, components=[boutonvote])
                on_click3 = msg3.create_click_listener(timeout=15)

                @on_click3.no_checks(cancel_others=False, reset_timeout=False)
                async def no_checks(inter):
                    jeux[inter.author][5] = inter.component.custom_id
                    await inter.reply(content="Vous avez bien choisis de voter contre : " + inter.component.label,
                                      ephemeral=True)

                @on_click3.timeout
                async def on_timeout():
                    listedevote = []
                    for key in jeux.keys():
                        if jeux[key][5] == "vote":
                            jeux[key][5] = key
                            listedevote.append(key)
                        else:
                            user = await bot.fetch_user(jeux[key][5])
                            jeux[key][5] = user
                            listedevote.append(user)
                    votefinaldelamort = max(set(listedevote), key=listedevote.count)
                    votetiret = ""
                    embed = discord.Embed(title="Votes",
                                          description="C'est l'heure de connaïtre les résultats des votes !",
                                          color=0x00ff00)
                    embed.set_footer(text="En cas d'égalité la personne éliminée sera choisie au hasard")
                    msgdevote = await chan.send(embed=embed)
                    await asyncio.sleep(2)
                    for key in jeux.keys():
                        votetiret += "-**" + key.mention + "** a voté **" + jeux[key][5].mention + "**\n"
                        embed = discord.Embed(title="Votes",
                                              description="C'est l'heure de connaïtre les résultats des votes !",
                                              color=0x00ff00)
                        embed.add_field(name="Votes", value=votetiret, inline=False)
                        embed.set_footer(text="En cas d'égalité la personne éliminée sera choisie au hasard")
                        await msgdevote.edit(embed=embed)
                        await asyncio.sleep(2)
                    await asyncio.sleep(3)
                    if jeux[votefinaldelamort][0] == "Civil":
                        embed = discord.Embed(title="Votes",
                                              description="C'est l'heure de connaïtre les résultats des votes !",
                                              color=0x00ff00)
                        embed.add_field(name="Votes",
                                        value="La personne éliminé est donc : " + votefinaldelamort.mention + "\nC'etais un **civil**",
                                        inline=False)
                        embed.set_footer(text="Victoire de l'undercover !")
                    else:
                        embed = discord.Embed(title="Votes",
                                              description="C'est l'heure de connaïtre les résultats des votes !",
                                              color=0x00ff00)
                        embed.add_field(name="Votes",
                                        value="La personne éliminé est donc : " + votefinaldelamort.mention + "\nC'etais un **undercover**",
                                        inline=False)
                        embed.set_footer(text="Victoire des civils !")
                    await msgdevote.edit(embed=embed)
                    await asyncio.sleep(10)
                    await chan.send("Fermeture du channel en cours ...")
                    await chan.delete()






        else:
            embed = discord.Embed(
                title="Undercover", description="Etat de la partie : **Annulé**", color=0xff0000)
            embed.set_footer(text="Le temps d'attente est terminé")
            await msg.edit(embed=embed, components=[])

