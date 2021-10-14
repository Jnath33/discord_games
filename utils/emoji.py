import discord

carte_deck = {}


def set(guild):
    global carte_deck
    for signe in [("♥", "heart"), ("♦", "diamond"), ("♣", "club"), ("♠", "spade")]:
        for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "V", "Q", "K"]:
            carte_deck[num + signe[0]] = [discord.utils.get(guild.emojis,
                                                            name=("b" if signe[0] in ["♣", "♠"] else "r") + num),
                                          discord.utils.get(guild.emojis,
                                                            name=signe[1])]
