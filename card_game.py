import random

import discord
from dislash import ActionRow, Button, ButtonStyle

ids = {}
id_to_totalname = {"n": "Nord", "s": "Sud", "e": "Est", "o": "Ouest"}


class Game:
    def __init__(self, players, inter, ctx):
        self.players = players
        self.inter = inter
        self.id = 0
        for i in range(10):
            c_id = random.randint(1, 10000)
            if c_id not in ids:
                self.id = c_id
        self.can_start = not self.id == 0
        self.ctx = ctx
        self.channel = None
        self.p_to_inter = {}

    async def end_init(self):
        guild = self.ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        for it in self.players.values():
            overwrites[it] = discord.PermissionOverwrite(read_messages=True)
        self.channel = await self.ctx.channel.category.create_text_channel("game-card-" + str(self.id),
                                                                           overwrites=overwrites)

    async def start(self):
        print(f"Game {self.id} is starting")
        msg = await self.channel.send(self.players["n"].mention + self.players["s"].mention +
                                      self.players["e"].mention + self.players["o"].mention)
        embed = discord.Embed(color=0xff8800)

        yes_button = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Oui",
                custom_id="y"
            )
        )
        embed.set_footer(text="This game was made by Jnath#5924")
        embed.add_field(name="Belote", value="ㅤ")
        await msg.edit(content="", embed=embed, components=[yes_button])
        for i in self.players.keys():
            embed = self.get_ready_msg(embed, i)
            await msg.edit(content="", embed=embed, components=[yes_button])

            def check(inter):
                if inter.message.id == msg.id and self.players[i] == inter.author:
                    self.p_to_inter[i] = inter
                    return True
                return False

            c_i = await msg.wait_for_button_click(check)
            await c_i.create_response(content="Votre Main : ("+id_to_totalname[i]+")", ephemeral=True, components=[yes_button])

            embed = self.get_ready_msg(embed, i)
            await msg.edit(content="", embed=embed, components=[])

    def get_ready_msg(self, embed, i):
        embed.set_field_at(index=0,
                            name="Belote",
                           value="ㅤ" +
                                 "\nJoueur Nord : " + (
                                     "[READY]" if "n" in self.p_to_inter else "[NOT READY]") +
                                 "\nJoueur Sud : " + (
                                     "[READY]" if "s" in self.p_to_inter else "[NOT READY]") +
                                 "\nJoueur Est : " + (
                                     "[READY]" if "e" in self.p_to_inter else "[NOT READY]") +
                                 "\nJoueur Ouest : " + (
                                     "[READY]" if "o" in self.p_to_inter else "[NOT READY]") +
                                 "\n\n" + id_to_totalname[i] + " est tu pret"
                           )
        return embed
