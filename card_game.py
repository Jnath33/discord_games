import random

import discord
from dislash import ActionRow, Button, ButtonStyle

import card

ids = {}
id_to_totalname = {"n": "Nord", "s": "Sud", "e": "Est", "o": "Ouest"}
pos_to_relative_pos = {"n": {"s": "n", "o": "e", "n": "s", "e": "o"},
                       "s": {"s": "s", "n": "n", "o": "o", "e": "e"},
                       "e": {"s": "o", "n": "e", "o": "n", "e": "s"},
                       "o": {"s": "e", "n": "o", "o": "s", "e": "n"}}


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
        self.p_to_inter = {}
        self.channels = {}

    async def end_init(self):
        guild = self.ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        for it in self.players.keys():
            overwrites[self.players[it]] = discord.PermissionOverwrite(read_messages=True)
            self.channels[it] = await self.ctx.channel.category.create_text_channel("game-card-" + id_to_totalname[it]
                                                                                    + "-" + str(self.id),
                                                                                    overwrites=overwrites)
            del overwrites[self.players[it]]

    async def start(self):
        print(f"Game {self.id} is starting")
        msgs = {"n": await self.channels["n"].send(self.players["n"].mention),
                "s": await self.channels["s"].send(self.players["s"].mention),
                "e": await self.channels["e"].send(self.players["e"].mention),
                "o": await self.channels["o"].send(self.players["o"].mention)}
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
        for i in self.players.keys():
            embed = self.get_ready_msg(embed, i)
            await edits(msgs, content="", embed=embed)
            await msgs[i].edit(components=[yes_button])

            def check(inter):
                if inter.message.id == msgs[i].id and self.players[i] == inter.author:
                    self.p_to_inter[i] = inter
                    return True
                return False

            c_i = await msgs[i].wait_for_button_click(check)
            await c_i.reply(content="a", type=6)

            await msgs[i].edit(components=[])
            embed = self.get_ready_msg(embed, i)

        await self.edits_game_message(embed,
                                      {"n": card.Card(card.Color.CARREAUX, 11, self.players["n"]),
                                            "e": card.Card(card.Color.COEUR, 8, self.players["e"]),
                                            "s": card.Card(card.Color.CARREAUX, 10, self.players["s"])},
                                      msgs)
        await edits(msgs, content="", embed=embed, components=[])

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

    async def edits_game_message(self, embed, val, msgs):
        for i in self.players.keys():
            embed.set_field_at(index=0,
                               name="Belote",
                               value="ㅤ" +
                                     "\nㅤㅤㅤㅤ" + (val[pos_to_relative_pos[i]["n"]].color.value["emoji"] +
                                                card.nomber_to_name[val[pos_to_relative_pos[i]["n"]].nomber]
                                                if pos_to_relative_pos[i]["n"] in val else
                                                "ㅤㅤ") +
                                     "\n\n" + (val[pos_to_relative_pos[i]["n"]].color.value["emoji"] +
                                               card.nomber_to_name[val[pos_to_relative_pos[i]["n"]].nomber]
                                               if pos_to_relative_pos[i]["n"] in val else
                                               "ㅤㅤ") + "\nㅤㅤㅤㅤㅤㅤㅤㅤ" +
                                     (val[pos_to_relative_pos[i]["n"]].color.value["emoji"] +
                                      card.nomber_to_name[val[pos_to_relative_pos[i]["n"]].nomber]
                                      if pos_to_relative_pos[i]["n"] in val else
                                      "ㅤㅤ") +
                                     "\n\nㅤㅤㅤ" + (
                                         val[pos_to_relative_pos[i]["n"]].color.value["emoji"] +
                                         card.nomber_to_name[val[pos_to_relative_pos[i]["n"]].nomber]
                                         if pos_to_relative_pos[i]["n"] in val else
                                         "ㅤㅤ") + "\n"
                               )
            await msgs[i].edit(embed=embed)


async def edits(msgs, **kwargs):
    for msg in msgs.values():
        await msg.edit(**kwargs)
