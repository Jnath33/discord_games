import random

import discord

from utils import lobby

ids = {}


class Game:
    def __init__(self, players, guild):
        self.id = 0
        for i in range(10):
            c_id = random.randint(1, 10000)
            if c_id not in ids:
                self.id = c_id
                break
        ids[self.id] = self
        can_start = not self.id == 0
        self.players = players
        self.guild = guild
        self.channel = None

    async def end_init(self, channel):
        guild = self.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        for it in self.players:
            overwrites[self.players] = discord.PermissionOverwrite(read_messages=True)

        self.channel = await self.channel.category.create_text_channel("pendu-game-" + str(self.id),
                                                                       overwrites=overwrites)


