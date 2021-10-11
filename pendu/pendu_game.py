import asyncio
import random

import discord

from utils import lobby

pendu = [
    "```\n" +
    "ㅤ\n" +
    "ㅤ\n" +
    "ㅤ\n" +
    "ㅤ\n" +
    "ㅤㅤㅤㅤㅤㅤ\n" +
    "```\n",
    "```\n" +
    "ㅤ\n" +
    "ㅤ\n" +
    "ㅤ\n" +
    "ㅤ\n" +
    "------+--\n" +
    "```\n",
    "```\n" +
    "      | \n" +
    "      | \n" +
    "      | \n" +
    "      |\n" +
    "------+--\n" +
    "``` \n",
    "``` \n" +
    "  ----+ \n" +
    "      | \n" +
    "      | \n" +
    "      | \n" +
    "------+--\n" +
    "``` \n",
    "``` \n" +
    "  ----+ \n" +
    "     \| \n" +
    "      | \n" +
    "      | \n" +
    "------+--\n" +
    "``` \n",
    "``` \n" +
    "  +---+ \n" +
    "  o  \| \n" +
    "      | \n" +
    "      | \n" +
    "------+--\n" +
    "```    \n",
    "```  \n" +
    "  +---+ \n" +
    "  o  \| \n" +
    "  |   | \n" +
    "      | \n" +
    "------+--\n" +
    "```     \n",
    "```     \n" +
    "  +---+ \n" +
    "  o  \| \n" +
    "  |   | \n" +
    "  ^   | \n" +
    "------+--\n" +
    "```     \n"]

ids = {}
with open("pendu/words", "r") as f:
    words = f.read().split("\n")


async def verif_message(bot_id, channel, message):
    if message.author.bot:
        return
    info = channel.name.split("-")
    if len(info) == 3 and info[1] == "pendu_game":
        if info[0] == bot_id:
            await message.delete()
            await ids[int(info[2])].update(message)


class Game:
    def __init__(self, players, channel):
        self.id = 0
        for i in range(10):
            c_id = random.randint(1, 10000)
            if c_id not in ids:
                self.id = c_id
                break
        ids[self.id] = self
        self.can_start = not self.id == 0
        self.players = players
        self.guild = channel.guild
        self.channel = channel
        self.d_channel = channel
        self.word = random.choice(words).lower()
        self.alredy_say_letter = []
        self.false_letter = []
        self.g_message = None
        self.end = False

    async def end_init(self, bot):
        guild = self.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        for it in self.players:
            overwrites[it] = discord.PermissionOverwrite(read_messages=True)
        tmp_channel = self.channel
        self.channel = await tmp_channel.category.create_text_channel(bot + "-pendu_game-" + str(self.id),
                                                                      overwrites=overwrites)
        txt = ""
        for p in self.players:
            txt += " " + p.mention
        self.g_message = await self.channel.send(txt, embed=self.get_embed())

        await self.g_message.edit(content="ㅤ")

    async def update(self, message):
        if self.can_start and not self.end:
            letter = message.content[0].lower()
            if 97 <= ord(letter) <= 122:
                if letter in self.alredy_say_letter:
                    await message.channel.send("Vous ne pouvez pas dire : " + letter + " ça a déjà était dit",
                                               delete_after=10)
                else:
                    if not letter in self.word:
                        self.false_letter.append(letter)
                    self.alredy_say_letter.append(letter)
                    await self.g_message.edit(embed=self.get_embed())
                    if len(self.false_letter) >= 7:
                        self.end = True
                        losse_embed = discord.Embed(name="Pendu", color=0xff0000)
                        losse_embed.add_field(name="Perdu :", value="Le mot était **" +
                                                                    self.word[0].upper() + self.word[1::] + "**")
                        await self.d_channel.send(embed=losse_embed)
                        await asyncio.sleep(.5)
                        await self.channel.delete()
                    win = True
                    for let in self.word:
                        if let not in self.alredy_say_letter:
                            win = False
                    if win:
                        self.end = True
                        win_embed = discord.Embed(name="Pendu", color=0x37ff00)
                        win_embed.add_field(name="Gagner :", value="Le mot était bien **" +
                                                                   self.word[0].upper() + self.word[1::] + "**")
                        await self.d_channel.send(embed=win_embed)
                        await asyncio.sleep(.5)
                        await self.channel.delete()

    def get_embed(self):
        embed = discord.Embed(title="Pendu :", color=0xff8800)
        play_let = []
        for let in self.false_letter:
            play_let.append(":regional_indicator_" + let + ":")

        embed.add_field(name="Pendu", value=pendu[min(len(self.false_letter), 7)])
        word = ""
        for let in self.word:
            if let in self.alredy_say_letter:
                word += ":regional_indicator_" + let + ":"
            else:
                word += "`_` "
        embed.add_field(name="Word", value=word)
        embed.add_field(name="Lettre fausse", value="ㅤ" if len(play_let) == 0 else ", ".join(play_let))

        return embed
