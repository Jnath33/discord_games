import discord
from dislash import ActionRow, Button, ButtonStyle
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
        ActionRow(Button(label="Go", style=ButtonStyle.green, custom_id="start"),
                  Button(label="ULTRA HARD MODE", style=ButtonStyle.red, custom_id="hardmode"))
    ])

    def check_menu(inter):
        return inter.author.id == author.id and msg[author.id].id == inter.message.id

    inter = await msg[author.id].wait_for_button_click(check_menu)
    await inter.reply(content="test", type=6, fetch_response_message=False)

    await on_button_click(inter)


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
        buttons[i_let] = ActionRow()
        for i in range(1, 6):
            buttons[i_let].buttons.append(
                Button(emoji=color_list[colors[i_let][i]][2], style=ButtonStyle.grey, custom_id=i_let + str(i))
            )

    userColorList[ctx.author.id] = win_color, \
                                   [list(colors["A"].values()),
                                    list(colors["B"].values()),
                                    list(colors["C"].values()),
                                    list(colors["D"].values())]

    await msg[ctx.author.id].edit(embed=embed,
                                  components=[buttons["A"],
                                              buttons["B"],
                                              buttons["C"],
                                              buttons["D"]])

    def check_game(inter):
        return inter.author.id == ctx.author.id and inter.message.id == ctx.message.id

    inter = await msg[ctx.author.id].wait_for_button_click(check_game)
    await inter.reply(content="test", type=6, fetch_response_message=False)

    await on_button_click(inter)


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
    if interaction.clicked_button.custom_id == "start":
        userTime[interaction.author.id] = time.time()
        userScore[interaction.author.id] = ""
        if interaction.author.id in userUltraHardMode:
            del userUltraHardMode[interaction.author.id]
        await game(interaction)
        userTime[interaction.author.id] = time.time()
        return
    if interaction.clicked_button.custom_id == "stop":
        userScore[interaction.author.id] = ""
        embed = discord.Embed(title="ColorZ", description="La partie est terminé", color=0xE1E1E1)
        await msg[interaction.author.id].edit(embed=embed, components=[])

    # Bouton pour le hard mode
    if interaction.clicked_button.custom_id == "hardmode":
        userScore[interaction.author.id] = ""
        embed = discord.Embed(title="ColorZ ULTRA HARD MODEEEEEEE",
                              description="Le ColorZ hard mode rend aléatoire les couleurs cliquées suivant des "
                                          "couleurs annoncée au début",
                              color=0xdd2e44)
        embed.add_field(name="Exemple :",
                        value="Si on vous demande de cliquer sur du bleu et qu'au début de la parti on vous à dis que "
                              "bleu=vert vous devez cliquer sur du vert !",
                        inline=False)
        button = [ActionRow(Button(style=ButtonStyle.green, label="Voir mes couleurs", custom_id="hardmodeStart"),
                            Button(style=ButtonStyle.red, label="Normal Mode", custom_id="normalmode"))]

        await msg[interaction.author.id].edit(embed=embed, components=button)

        def check(inter):
            return inter.author.id == interaction.author.id and inter.message.id == interaction.message.id

        inter = await msg[interaction.author.id].wait_for_button_click(check)
        await inter.reply(content="test", type=6, fetch_response_message=False)

        await on_button_click(inter)
        return
    if interaction.clicked_button.custom_id == "hardmodeStart":
        userTime[interaction.author.id] = time.time()
        userScore[interaction.author.id] = ""
        color = await color_hard()
        userUltraHardMode[interaction.author.id] = [color, True]
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
        button = [ActionRow(Button(style=ButtonStyle.green, label="GOOOOOOOOO !!!", custom_id="hardmodeGame"))]

        await msg[interaction.author.id].edit(embed=embed, components=button)

        def check(inter):
            return inter.author.id == interaction.author.id and inter.message.id == interaction.message.id

        inter = await msg[interaction.author.id].wait_for_button_click(check)
        await inter.reply(content="test", type=6, fetch_response_message=False)
        await on_button_click(inter)
        return

    if interaction.clicked_button.custom_id == "hardmodeGame":
        userScore[interaction.author.id] = ""
        await game(interaction)
        return

    if interaction.clicked_button.custom_id == "normalmode":
        userScore[interaction.author.id] = ""
        embed = discord.Embed(title="ColorZ",
                              description="Appuyez sur les bonnes couleurs le plus vite possible.\nprêt ?",
                              color=0xE1E1E1)
        msg[interaction.author.id] = await interaction.edit(embed=embed, components=[
            ActionRow(Button(label="Go", style=ButtonStyle.green, custom_id="start"),
                      Button(label="ULTRA HARD MODE", style=ButtonStyle.red, custom_id="hardmode"))])

        def check(inter):
            return inter.author.id == interaction.author.id and inter.message.id == interaction.message.id

        inter = await msg[interaction.author.id].wait_for_button_click(check)
        await inter.reply(content="test", type=6, fetch_response_message=False)
        await on_button_click(inter)
        return

        # Bouton ligne A cliqué
    c_to_l = ["A", "B", "C", "D"]

    def c_to_c(c):
        return c + 1

    find = False
    for let in range(4):
        for chi in range(5):
            if interaction.clicked_button.custom_id == c_to_l[let] + str(c_to_c(chi)):
                if userColorList[interaction.author.id][0] == userColorList[interaction.author.id][1][let][chi]:
                    userScore[interaction.author.id] += "1"
                else:
                    userScore[interaction.author.id] += "0"
                if len(userScore[interaction.author.id]) != 5:
                    await game(interaction)
                find = True
                break
        if find:
            break

    if len(userScore[interaction.author.id]) == 5:
        time_end = time.time()
        time_total = round(time_end - userTime[interaction.author.id], 3)
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
        del userScore[interaction.author.id]
        await msg[interaction.author.id].edit(embed=embed, components=[
            ActionRow(Button(label="Recommencer ?", custom_id=id_button, style=ButtonStyle.green),
                      Button(label="Arreter ?", custom_id="stop", style=ButtonStyle.red))])

        def check(inter):
            return inter.author.id == interaction.author.id and inter.message.id == interaction.message.id

        inter = await msg[interaction.author.id].wait_for_button_click(check)
        await inter.reply(content="test", type=6, fetch_response_message=False)
        await on_button_click(inter)


async def add_leaderboard(ctx, time):
    global userUltraHardMode
    fichier = "color_z/leaderboard.csv"
    if ctx.author.id in userUltraHardMode:
        if userUltraHardMode[ctx.author.id][1]:
            fichier = "color_z/leaderboardHard.csv"

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


async def lb(channel, author, *hard):
    fichier = "color_z/leaderboard.csv"
    embed = discord.Embed(title="ColorZ", color=0xE1E1E1)
    if "hard" in hard:
        fichier = "color_z/leaderboardHard.csv"
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
