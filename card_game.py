import random

import discord
from dislash import ActionRow, Button, ButtonStyle

import card

ids = {}
id_to_totalname = {"n": "Nord", "s": "Sud", "e": "Est", "o": "Ouest"}
pos_to_relative_pos = {"n": {"s": "n", "o": "e", "n": "s", "e": "o"},
                       "s": {"s": "s", "n": "n", "o": "o", "e": "e"},
                       "e": {"s": "e", "n": "o", "o": "s", "e": "n"},
                       "o": {"s": "o", "n": "e", "o": "n", "e": "s"}}
get_next = {"n": "e", "e": "s", "s": "o", "o": "n"}

c_id_to_c = {
    "co": card.Color.COEUR,
    "ca": card.Color.CARREAUX,
    "tr": card.Color.TREFLE,
    "pi": card.Color.PIQUE,
    None: None
}


class Game:
    def __init__(self, players, inter, ctx):
        self.cards = []
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
        self.hand_card = {"n": [], "s": [], "o": [], "e": []}
        self.make_cards_list()
        self.distribue(5)

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
        yes_no_button = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Oui",
                custom_id="y"
            ),
            Button(
                style=ButtonStyle.red,
                label="Non",
                custom_id="n"
            )
        )
        deux_button = ActionRow(
            Button(
                style=ButtonStyle.gray,
                label="",
                custom_id="co",
                emoji="❤️"
            ),
            Button(
                style=ButtonStyle.gray,
                label="",
                custom_id="ca",
                emoji="♦️"
            ),
            Button(
                style=ButtonStyle.gray,
                label="",
                custom_id="tr",
                emoji="♣️"
            ),
            Button(
                style=ButtonStyle.gray,
                label="",
                custom_id="pi",
                emoji="♠️"
            ),
            Button(
                style=ButtonStyle.red,
                label="Deux",
                custom_id="de"
            )
        )
        embed = discord.Embed(color=0xff8800)
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

        embed = discord.Embed(color=0x37ff00)
        embed.set_footer(text="This game was made by Jnath#5924")
        embed.add_field(name="Belote", value="ㅤ")

        next_player_to_play = "n"

        embed.set_field_at(0,
                           name="Belote",
                           value="ㅤ\nㅤ" + self.cards[0].color.value["emoji"] + card.nomber_to_name[
                               self.cards[0].nomber] +
                                 "\nㅤ")
        await edits(msgs, embed=embed)

        p_second = True
        run = True

        while run:
            for i in self.players:
                await msgs[i].edit(components=card.to_buttons(self.hand_card[i], []))

            for i in start_player_to_play_list(next_player_to_play):
                await msgs[i].edit(components=card.to_buttons(self.hand_card[i], []) + [yes_no_button])

                def check(inter):
                    return inter.message.id == msgs[i].id and self.players[i] == inter.author

                inter = await msgs[i].wait_for_button_click(check)
                await inter.reply(content="a", type=6)

                await msgs[i].edit(components=card.to_buttons(self.hand_card[i], []))
                if inter.clicked_button.custom_id == "y":
                    card.atout_color = self.cards[0].color
                    p_second = False
                    run = False
                    next_player_to_play = i
                    for it in start_player_to_play_list(i):
                        self.distribue(3, it)
                    break

            if p_second:
                for i in start_player_to_play_list(next_player_to_play):
                    await msgs[i].edit(components=card.to_buttons(self.hand_card[i], []) + [deux_button])

                    def check(inter):
                        return inter.message.id == msgs[i].id and self.players[i] == inter.author

                    inter = await msgs[i].wait_for_button_click(check)
                    await inter.reply(content="a", type=6)

                    await msgs[i].edit(components=card.to_buttons(self.hand_card[i], []))
                    if inter.clicked_button.custom_id != "de":
                        card.atout_color = c_id_to_c[inter.clicked_button.custom_id]
                        next_player_to_play = i
                        run = False
                        for it in start_player_to_play_list(i):
                            self.distribue(3, it)
                        break
            if run:
                self.make_cards_list()
                self.hand_card = {"n": [], "s": [], "o": [], "e": []}
                self.distribue(5)
                embed.set_field_at(0,
                                   name="Belote",
                                   value="ㅤ\nㅤ" + self.cards[0].color.value["emoji"] + card.nomber_to_name[
                                       self.cards[0].nomber] + "\nㅤ")
                await edits(msgs, embed=embed)

                next_player_to_play = get_next[next_player_to_play]

        for i in self.players:
            await msgs[i].edit(components=card.to_buttons(self.hand_card[i], []))

        embed.add_field(name="Score",
                        value="ㅤ\n\n\nAtouts : " + card.atout_color.value["emoji"] + "\n",
                        inline=False)
        embed.add_field(name="C'est le tour de",
                        value="ㅤ",
                        inline=True)

        for i in range(8):
            card_played = {}
            card_color = None
            for it in start_player_to_play_list(next_player_to_play):
                embed.set_field_at(index=2,
                                   name="C'est le tour de",
                                   value="ㅤ" + self.players[it].name + " (" + id_to_totalname[it] +
                                         ")",
                                   inline=True)
                for ite in self.players:
                    await msgs[ite].edit(embed=self.get_game_message(embed, card_played, ite))
                await msgs[it].edit(components=card.to_buttons(self.hand_card[it],
                                                               card.get_playable(self.hand_card[it],
                                                                                 card_color)))

                def check(inter):
                    b_id = inter.clicked_button.custom_id.split("-")
                    if inter.message.id == msgs[it].id and self.players[it] == inter.author:
                        card_played[it] = card.Card(c_id_to_c[b_id[0]], int(b_id[1]))
                        c_player_hand = self.hand_card[it]
                        d_n = None
                        for c in range(len(c_player_hand)):
                            if str(c_player_hand[c]) == inter.clicked_button.custom_id:
                                d_n = c
                        del self.hand_card[it][d_n]
                        card_played[str(card.Card(c_id_to_c[b_id[0]], int(b_id[1])))] = it
                        return True
                    return False

                inter = await msgs[it].wait_for_button_click(check)
                await msgs[it].edit(components=card.to_buttons(self.hand_card[it], []))
                if card_color is None:
                    card_color = c_id_to_c[inter.clicked_button.custom_id.split("-")[0]]
                await inter.reply(content="c", type=6)
            next_player_to_play = card_played[str(card.beats(card_color, list(card_played.values())))]
            print(self.hand_card)

        for msg in msgs.values():
            await msg.channel.delete()

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

    def get_game_message(self, embed, val, i):
        embed.set_field_at(index=0,
                           name="Belote",
                           value="ㅤ" +
                                 "\nㅤㅤㅤㅤ" + (val[pos_to_relative_pos[i]["n"]].color.value["emoji"] +
                                             card.nomber_to_name[val[pos_to_relative_pos[i]["n"]].nomber]
                                             if pos_to_relative_pos[i]["n"] in val else
                                             "ㅤㅤ") +
                                 "\n\n" + (val[pos_to_relative_pos[i]["o"]].color.value["emoji"] +
                                           card.nomber_to_name[val[pos_to_relative_pos[i]["o"]].nomber]
                                           if pos_to_relative_pos[i]["o"] in val else
                                           "ㅤㅤ") + "\nㅤㅤㅤㅤㅤㅤㅤㅤ" +
                                 (val[pos_to_relative_pos[i]["e"]].color.value["emoji"] +
                                  card.nomber_to_name[val[pos_to_relative_pos[i]["e"]].nomber]
                                  if pos_to_relative_pos[i]["e"] in val else
                                  "ㅤㅤ") +
                                 "\n\nㅤㅤㅤㅤ" + (
                                     val[pos_to_relative_pos[i]["s"]].color.value["emoji"] +
                                     card.nomber_to_name[val[pos_to_relative_pos[i]["s"]].nomber]
                                     if pos_to_relative_pos[i]["s"] in val else
                                     "ㅤㅤ") + "\n"
                           )
        return embed

    def distribue(self, card, player=None):
        if player is None:
            for i in self.players:
                self.hand_card[i] += self.cards[0:card]
                del self.cards[0:card]
        else:
            self.hand_card[player] += self.cards[0:card]
            del self.cards[0:card]

    def make_cards_list(self):
        t_cards = [[card.Card(i, m) for m in range(7, 14)] for i in [card.Color.COEUR,
                                                                     card.Color.TREFLE,
                                                                     card.Color.CARREAUX,
                                                                     card.Color.PIQUE]]
        self.cards = []
        for i in t_cards:
            self.cards += i
        for i in [card.Color.COEUR,
                  card.Color.TREFLE,
                  card.Color.CARREAUX,
                  card.Color.PIQUE]:
            self.cards.append(card.Card(i, 1))

        random.shuffle(self.cards)


async def edits(msgs, **kwargs):
    for msg in msgs.values():
        await msg.edit(**kwargs)


def start_player_to_play_list(f_p, s=None, l=None):
    if l is None:
        l = []
    if f_p == s:
        return l
    else:
        l.append(f_p)
        if s is None:
            return start_player_to_play_list(get_next[f_p], f_p, l)
        else:
            return start_player_to_play_list(get_next[f_p], s, l)
