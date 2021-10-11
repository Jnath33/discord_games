import discord
import random
import time
import pandas as pd

msg = {}
userColorList = {}
userScore = {}
userTime = {}
userUltraHardMode = {}


async def colorz(channel, author):
    global msg
    global userScore
    userScore[author.id] = ""
    # Envoie l'embed de start
    embed = discord.Embed(title="ColorZ", description="Appuyez sur les bonnes couleurs le plus vite possible.\nprêt ?",
                          color=0xE1E1E1)
    msg[author.id] = await channel.send(embed=embed, components=[
        [Button(label="Go", style=ButtonStyle.green, id="start"),
         Button(label="ULTRA HARD MODE", style=ButtonStyle.red, id="hardmode")]])


async def game(ctx):
    global msg
    global userUltraHardMode
    global userColorList
    global userScore
    # Liste des couleurs avec leur ecritures hexa
    color_list = {"blanc": [0xe6e7e8, ":white_large_square:", "⬜"],
                  "orange": [0xf4900c, ":orange_square:", "🟧"],
                  "bleu": [0x55acee, ":blue_square:", "🟦"],
                  "rouge": [0xdd2e44, ":red_square:", "🟥"],
                  "marron": [0xc1694f, ":brown_square:", "🟫"],
                  "violet": [0xaa8ed6, ":purple_square:", "🟪"],
                  "vert": [0x78b159, ":green_square:", "🟩"],
                  "jaune": [0xfdcb58, ":yellow_square:", "🟨"]}

    # Randomize la couleur gagnante
    win_color = random.choice(list(color_list))
    win_color_hex = color_list[win_color][0]
    win_color_emoji = color_list[win_color][1]

    embed = discord.Embed(title="ColorZ", description=win_color_emoji + "Appuyez sur du " + win_color + ".",
                          color=win_color_hex)

    if ctx.author.id in userUltraHardMode:
        if userUltraHardMode[ctx.author.id][1]:
            color_list = userUltraHardMode[ctx.author.id][0]
    # Declaration des bouttons par ligne avec leur couleur attitré

    colors = {}
    all_color = set()

    for i_let in ["A", "B", "C", "D"]:
        colors[i_let] = {}
        for i in range(1, 6):
            colors[i_let][i] = random.choice(list(color_list))
            all_color.add(colors[i_let][i])

    if win_color not in all_color:
        colors[random.choice(["A", "B", "C", "D"])][random.randint(1, 5)] = win_color

    buttons = {}

    for i_let in ["A", "B", "C", "D"]:
        buttons[i_let] = []
        for i in range(1, 6):
            buttons[i_let].append(
                Button(emoji=color_list[colors[i_let][i]][2], style=ButtonStyle.grey, id=i_let + str(i))
            )

    userColorList[ctx.author.id] = win_color, \
                                   [colors["A"].values(),
                                    colors["B"].values(),
                                    colors["C"].values(),
                                    colors["D"].values()]

    await msg[ctx.author.id].edit(embed=embed,
                                  components=[buttons["A"],
                                              buttons["B"],
                                              buttons["C"],
                                              buttons["D"]])


async def color_hard():
    color_name = [[0xe6e7e8, ":white_large_square:", "⬜"],
                  [0xf4900c, ":orange_square:", "🟧"],
                  [0x55acee, ":blue_square:", "🟦"],
                  [0xdd2e44, ":red_square:", "🟥"],
                  [0xc1694f, ":brown_square:", "🟫"],
                  [0xaa8ed6, ":purple_square:", "🟪"],
                  [0x78b159, ":green_square:", "🟩"],
                  [0xfdcb58, ":yellow_square:", "🟨"]]

    color_list = {"blanc": "",
                  "orange": "",
                  "bleu": "",
                  "rouge": "",
                  "marron": "",
                  "violet": "",
                  "vert": "",
                  "jaune": ""}

    random.shuffle(color_name)
    for i in range(len(color_name)):
        if color_name[i] != [0xe6e7e8, ":white_large_square:", "⬜"]:
            color_list["blanc"] = color_name[i]
            del color_name[i]
            break

    for i in range(len(color_name)):
        if color_name[i] != [0xf4900c, ":orange_square:", "🟧"]:
            color_list["orange"] = color_name[i]
            del color_name[i]
            break

    for i in range(len(color_name)):
        if color_name[i] != [0x55acee, ":blue_square:", "🟦"]:
            color_list["bleu"] = color_name[i]
            del color_name[i]
            break

    for i in range(len(color_name)):
        if color_name[i] != [0xdd2e44, ":red_square:", "🟥"]:
            color_list["rouge"] = color_name[i]
            del color_name[i]
            break

    for i in range(len(color_name)):
        if color_name[i] != [0xc1694f, ":brown_square:", "🟫"]:
            color_list["marron"] = color_name[i]
            del color_name[i]
            break

    for i in range(len(color_name)):
        if color_name[i] != [0xaa8ed6, ":purple_square:", "🟪"]:
            color_list["violet"] = color_name[i]
            del color_name[i]
            break

    for i in range(len(color_name)):
        if color_name[i] != [0x78b159, ":green_square:", "🟩"]:
            color_list["vert"] = color_name[i]
            del color_name[i]
            break

    if color_name[0] != [0xfdcb58, ":yellow_square:", "🟨"]:
        color_list["jaune"] = color_name[0]

    else:
        ran = random.randint(0, len(color_list) - 2)
        color_list["jaune"] = color_list[list(color_list.keys())[ran]]
        color_list[list(color_list.keys())[ran]] = color_name[0]

    return color_list


async def on_button_click(interaction):
    global userColorList
    global msg
    global userScore
    global userTime
    global userUltraHardMode

    # Verifie quel bouton est appuyer, 123=Colonne et ABC    =Ligne
    if interaction.component.id == "start":
        userScore[interaction.author.id] = ""
        await interaction.respond(type=6, content="test")
        await game(interaction)
        userTime[interaction.author.id] = time.time()
    if interaction.component.id == "stop":
        userScore[interaction.author.id] = ""
        await interaction.respond(type=6, content="test")
        embed = discord.Embed(title="ColorZ", description="La partie est terminé", color=0xE1E1E1)
        await msg[interaction.author.id].edit(embed=embed, components=[])

    # Bouton pour le hard mode
    if interaction.component.id == "hardmode":
        userScore[interaction.author.id] = ""
        await interaction.respond(type=6, content="test")
        embed = discord.Embed(title="ColorZ ULTRA HARD MODEEEEEEE",
                              description="Le ColorZ hard mode rend aléatoire les couleurs cliquées suivant des "
                                          "couleurs annoncée au début",
                              color=0xdd2e44)
        embed.add_field(name="Exemple :",
                        value="Si on vous demande de cliquer sur du bleu et qu'au début de la parti on vous à dis que "
                              "bleu=vert vous devez cliquer sur du vert !",
                        inline=False)
        button = [[Button(style=ButtonStyle.green, label="Voir mes couleurs", id="hardmodeStart"),
                   Button(style=ButtonStyle.red, label="Normal Mode", id="normalmode")]]
        await msg[interaction.author.id].edit(embed=embed, components=button)
    if interaction.component.id == "hardmodeStart":
        userTime[interaction.author.id] = time.time()
        userScore[interaction.author.id] = ""
        color = await color_hard()
        userUltraHardMode[interaction.author.id] = [color, True]
        await interaction.respond(type=6, content="test")
        text = ""
        color_list = {"blanc": [0xe6e7e8, ":white_large_square:", "⬜"],
                      "orange": [0xf4900c, ":orange_square:", "🟧"],
                      "bleu": [0x55acee, ":blue_square:", "🟦"],
                      "rouge": [0xdd2e44, ":red_square:", "🟥"],
                      "marron": [0xc1694f, ":brown_square:", "🟫"],
                      "violet": [0xaa8ed6, ":purple_square:", "🟪"],
                      "vert": [0x78b159, ":green_square:", "🟩"],
                      "jaune": [0xfdcb58, ":yellow_square:", "🟨"]}

        for key in color:
            text += color_list[key][1] + color_list[key][1] + color_list[key][1] + " ==> " + str(color[key][1]) + str(
                color[key][1]) + str(color[key][1]) + "\n"

        embed = discord.Embed(title="ColorZ ULTRA HARD MODEEEEEEE", color=0xdd2e44)
        embed.add_field(name="Vos couleurs :", value=text, inline=False)
        embed.set_footer(text="Le temps pour regarder les couleurs est aussi comptabilisé")
        button = [[Button(style=ButtonStyle.green, label="GOOOOOOOOO !!!", id="hardmodeGame")]]

        await msg[interaction.author.id].edit(embed=embed, components=button)

    if interaction.component.id == "hardmodeGame":
        userScore[interaction.author.id] = ""
        await interaction.respond(type=6, content="test")
        await game(interaction)

    if interaction.component.id == "normalmode":
        await interaction.respond(type=6, content="test")
        userScore[interaction.author.id] = ""
        embed = discord.Embed(title="ColorZ",
                              description="Appuyez sur les bonnes couleurs le plus vite possible.\nprêt ?",
                              color=0xE1E1E1)
        msg[interaction.author.id] = await interaction.edit(embed=embed, components=[
            [Button(label="Go", style=ButtonStyle.green, id="start"),
             Button(label="ULTRA HARD MODE", style=ButtonStyle.red, id="hardmode")]])

    # Bouton ligne A cliqué
    if interaction.component.id == "A1":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][0][0]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "A2":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][0][1]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "A3":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][0][2]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "A4":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][0][3]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "A5":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][0][4]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)

    # Bouton ligne B Cliqué
    if interaction.component.id == "B1":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][1][0]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "B2":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][1][1]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "B3":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][1][2]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "B4":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][1][3]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "B5":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][1][4]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)

    # Bouton ligne C Cliqué
    if interaction.component.id == "C1":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][2][0]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "C2":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][2][1]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "C3":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][2][2]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "C4":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][2][3]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "C5":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][2][4]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)

    # Bouton ligne D Cliqué
    if interaction.component.id == "D1":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][3][0]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "D2":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][3][1]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "D3":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][3][2]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "D4":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][3][3]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)
    if interaction.component.id == "D5":
        if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][3][4]:
            userScore[interaction.author.id] += "1"
        else:
            userScore[interaction.author.id] += "0"
        if len(userScore[interaction.author.id]) != 5:
            await interaction.respond(type=6, content="test")
            await game(interaction)

    if len(userScore[interaction.author.id]) == 5:
        time_end = time.time()
        time_total = round(time_end - userTime[interaction.author.id], 3)
        await interaction.respond(type=6, content="test")
        score_circle = ""
        score = 0
        for word in userScore[interaction.author.id]:
            if word == "1":
                score_circle += ":green_circle:"
                score += 1
            else:
                score_circle += ":red_circle:"
        best_score = ""
        if userScore[interaction.author.id] == "11111":
            best_score = await add_leaderboard(interaction, time_total)
            embed = discord.Embed(title="ColorZ", description="Vous avez Gagné", color=0x78b159)
        else:
            embed = discord.Embed(title="ColorZ", description="Vous avez Perdu", color=0xdd2e44)
        embed.add_field(name="Score " + str(score) + "/5", value=score_circle, inline=False)
        embed.add_field(name="Temps : ", value=best_score + str(time_total) + "s", inline=False)

        if interaction.author.id in userUltraHardMode:
            if userUltraHardMode[interaction.author.id][1]:
                id_button = "hardmodeStart"
            else:
                id_button = "start"
        else:
            id_button = "start"
        await msg[interaction.author.id].edit(embed=embed, components=[
            [Button(label="Recommencer ?", id=id_button, style=ButtonStyle.green),
             Button(label="Arreter ?", id="stop", style=ButtonStyle.red)]])


async def add_leaderboard(ctx, time):
    global userUltraHardMode
    fichier = "leaderboard.csv"
    if ctx.author.id in userUltraHardMode:
        if userUltraHardMode[ctx.author.id][1]:
            fichier = "leaderboardHard.csv"

    leaderboard = pd.read_table(fichier, sep=',', header=0)
    best_score = ""
    if ctx.author.mention in leaderboard['ID'].tolist():
        place = leaderboard['ID'].tolist().index(ctx.author.mention)
        if leaderboard.loc[place, "Time"] > time:
            leaderboard.loc[place, 'ID'] = ctx.author.mention
            leaderboard.loc[place, 'Time'] = time
            best_score = ":crown: "
    else:
        place = len(leaderboard['ID'].tolist())
        leaderboard.loc[place, 'ID'] = ctx.author.mention
        leaderboard.loc[place, 'Time'] = time
        best_score = ":crown: "
    leaderboard.to_csv(fichier, index=False)
    return best_score


async def lb(channel, author, hard):
    fichier = "leaderboard.csv"
    embed = discord.Embed(title="ColorZ", color=0xE1E1E1)
    if "hard" == hard:
        fichier = "leaderboardHard.csv"
        embed = discord.Embed(title="ColorZ Ultra Hard Mode", color=0xdd2e44)
    else:
        embed.set_footer(text="Faites \"!lb hard\" pour voir le leaderboard du hard mode")
    global msg
    leaderboard = pd.read_table(fichier, sep=',', header=0)
    value = 0
    total_value = []
    lb_time = leaderboard["Time"].to_list()
    user = []
    if len(lb_time) <= 10:
        a = len(lb_time)
    else:
        a = 10
    for i in range(a):
        for element in lb_time:
            if value == 0:
                value = element
            elif element < value:
                value = element
        delete_number = lb_time.index(float(value))
        del lb_time[delete_number]
        total_value.append(value)
        value = 0
    for element in total_value:
        place = leaderboard["Time"].to_list().index(element)
        user.append(leaderboard.loc[place, "ID"])

    text = ""
    i = 0
    for element in user:
        text += str(i + 1) + "-" + str(element) + " : " + str(total_value[i]) + "s\n"
        i += 1

    if author.mention in leaderboard["ID"].to_list():
        place = leaderboard["ID"].to_list().index(author.mention)
        embed.add_field(name="Votre score :", value=str(leaderboard.loc[place, "Time"]) + "s", inline=False)
    embed.add_field(name="LeaderBoard :", value=text, inline=False)
    await channel.send(embed=embed)
