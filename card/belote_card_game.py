import asyncio
import random

import discord
from dislash import ActionRow, Button, ButtonStyle

from card import belote_card

# set all the dic
ids = {}
id_to_total_name = {"n": "Nord", "s": "Sud", "e": "Est", "o": "Ouest"}
pos_to_relative_pos = {"n": {"s": "n", "o": "e", "n": "s", "e": "o"},
                       "s": {"s": "s", "n": "n", "o": "o", "e": "e"},
                       "e": {"s": "e", "n": "o", "o": "s", "e": "n"},
                       "o": {"s": "o", "n": "e", "o": "n", "e": "s"}}
get_next = {"n": "e", "e": "s", "s": "o", "o": "n"}
get_teammate = {"n": "s", "s": "n", "o": "e", "e": "o"}
player_to_team = {"n": "ns", "s": "ns", "o": "eo", "e": "eo"}
c_id_to_c = {
    "co": belote_card.Color.COEUR,
    "ca": belote_card.Color.CARREAUX,
    "tr": belote_card.Color.TREFLE,
    "pi": belote_card.Color.PIQUE,
    None: None
}


# return a the good message where i is the player id
def get_game_message(embed, val, i):
    embed.set_field_at(index=0,
                       name="Belote",
                       value="ㅤ" +
                             "\nㅤㅤㅤㅤ" + (val[pos_to_relative_pos[i]["n"]].color.value["emoji"] +
                                         belote_card.nomber_to_name[val[pos_to_relative_pos[i]["n"]].nomber]
                                         if pos_to_relative_pos[i]["n"] in val else
                                         "ㅤㅤ") +
                             "\n\n" + (val[pos_to_relative_pos[i]["o"]].color.value["emoji"] +
                                       belote_card.nomber_to_name[val[pos_to_relative_pos[i]["o"]].nomber]
                                       if pos_to_relative_pos[i]["o"] in val else
                                       "ㅤㅤ") + "\nㅤㅤㅤㅤㅤㅤㅤㅤ" +
                             (val[pos_to_relative_pos[i]["e"]].color.value["emoji"] +
                              belote_card.nomber_to_name[val[pos_to_relative_pos[i]["e"]].nomber]
                              if pos_to_relative_pos[i]["e"] in val else
                              "ㅤㅤ") +
                             "\n\nㅤㅤㅤㅤ" + (
                                 val[pos_to_relative_pos[i]["s"]].color.value["emoji"] +
                                 belote_card.nomber_to_name[val[pos_to_relative_pos[i]["s"]].nomber]
                                 if pos_to_relative_pos[i]["s"] in val else
                                 "ㅤㅤ") + "\n"
                       )
    return embed


# the main class
class Game:
    def __init__(self, players, inter, ctx, j_msg, point=1000):
        self.max_point = point
        self.j_msg = j_msg
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
        self.distribute(5)
        self.teams_score = {"global": {"ns": 0, "eo": 0},
                            "current": {"ns": 0, "eo": 0}}

    # add a end init because init can be async
    async def end_init(self):
        guild = self.ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        for it in self.players.keys():
            overwrites[self.players[it]] = discord.PermissionOverwrite(read_messages=True)
            self.channels[it] = await self.ctx.channel.category.create_text_channel("game-card-" + id_to_total_name[it]
                                                                                    + "-" + str(self.id),
                                                                                    overwrites=overwrites)
            del overwrites[self.players[it]]

    # the game
    async def start(self):

        print(f"Game {self.id} is starting")
        msgs = {"n": await self.channels["n"].send(self.players["n"].mention),
                "s": await self.channels["s"].send(self.players["s"].mention),
                "e": await self.channels["e"].send(self.players["e"].mention),
                "o": await self.channels["o"].send(self.players["o"].mention)}
        await edits(msgs, content="ㅤ")

        # Create used button yes/no for first turn and the four trump and the deux for the second turn

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
        two_button = ActionRow(
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

        # Create the embed
        embed = discord.Embed(color=0x37ff00)
        embed.set_footer(text="This game was made by Jnath#5924")
        embed.add_field(name="Belote", value="ㅤ")

        embed.add_field(name="ㅤ",
                        value="ㅤ",
                        inline=False)
        embed.add_field(name="Score",
                        value="ㅤ\n\n\ntrumps : " + belote_card.get_trump_color(self.id).value["emoji"] + "\n",
                        inline=True)
        embed.add_field(name="C'est le tour de",
                        value="ㅤ",
                        inline=True)

        # Define the first player to play
        start_player = "n"

        # main loop
        # this loop run util a team reach the objective
        while self.teams_score["global"]["ns"] < self.max_point and self.teams_score["global"]["eo"] < self.max_point:
            # the the first field to the card proposed
            embed.set_field_at(0,
                               name="Belote",
                               value="ㅤ\nㅤ" + self.cards[0].color.value["emoji"] + belote_card.nomber_to_name[
                                   self.cards[0].nomber] +
                                     "\nㅤ")
            # edits the messages with the new embed
            await edits(msgs, embed=embed)

            # Add some boolean for stop to the good time
            p_second = True
            run = True
            who_take_trump = None

            # first turn
            while run:
                for i in self.players:
                    await msgs[i].edit(components=belote_card.to_buttons(self.hand_card[i], []))

                for i in start_player_to_play_list(start_player):
                    await msgs[i].edit(components=belote_card.to_buttons(self.hand_card[i], []) + [yes_no_button])

                    def check(inter_first_turn):
                        return inter_first_turn.message.id == msgs[i].id and self.players[i] == inter_first_turn.author

                    inter = await msgs[i].wait_for_button_click(check)
                    await inter.reply(content="a", type=6)

                    await msgs[i].edit(components=belote_card.to_buttons(self.hand_card[i], []))
                    if inter.clicked_button.custom_id == "y":
                        belote_card.set_trump_color(self.id, self.cards[0].color)
                        p_second = False
                        run = False
                        who_take_trump = i
                        self.distribute(1, i)
                        break

                # second turn
                if p_second:
                    for i in start_player_to_play_list(start_player):
                        await msgs[i].edit(components=belote_card.to_buttons(self.hand_card[i], []) + [two_button])

                        def check(inter_second_turn):
                            return inter_second_turn.message.id == msgs[i].id and self.players[i] == \
                                   inter_second_turn.author

                        inter = await msgs[i].wait_for_button_click(check)
                        await inter.reply(content="a", type=6)

                        await msgs[i].edit(components=belote_card.to_buttons(self.hand_card[i], []))
                        if inter.clicked_button.custom_id != "de":
                            belote_card.set_trump_color(id, c_id_to_c[inter.clicked_button.custom_id])
                            run = False
                            who_take_trump = i
                            self.distribute(1, i)
                            break

                # redistribute the card if nothing was choose
                if run:
                    cut_int = random.randint(5, 27)
                    self.cards = self.cards[cut_int:32] + self.cards[0:cut_int]
                    self.hand_card = {"n": [], "s": [], "o": [], "e": []}
                    self.distribute(5)
                    embed.set_field_at(0,
                                       name="Belote",
                                       value="ㅤ\nㅤ" + self.cards[0].color.value["emoji"] + belote_card.nomber_to_name[
                                           self.cards[0].nomber] + "\nㅤ")
                    await edits(msgs, embed=embed)

                    start_player = get_next[start_player]

            # add missing card to the players
            bonus = {"ns": 0, "eo": 0}
            for i in self.players:
                self.distribute(8 - len(self.hand_card[i]), i)
                if belote_card.Card(
                        belote_card.get_trump_color(self.id), 12, belote_card.get_trump_color(self.id)
                ) in self.hand_card[i] and belote_card.Card(
                    belote_card.get_trump_color(self.id), 13, belote_card.get_trump_color(self.id)
                ) in self.hand_card[i]:
                    bonus[player_to_team[i]] += 20
                await msgs[i].edit(components=belote_card.to_buttons(self.hand_card[i], []))

            # set the next player who played to the start player
            next_player_to_play = start_player
            # A card turn
            for i in range(8):
                card_played = {}
                card_color = None
                embed = self.update_score(embed, self.teams_score)
                # a card duel
                for it in start_player_to_play_list(next_player_to_play):
                    embed.set_field_at(index=3,
                                       name="C'est le tour de",
                                       value="ㅤ" + self.players[it].name + " (" + id_to_total_name[it] +
                                             ")",
                                       inline=True)
                    for ite in self.players:
                        await msgs[ite].edit(embed=get_game_message(embed, card_played, ite))
                    await msgs[it].edit(components=belote_card.to_buttons(self.hand_card[it],
                                                                          belote_card.get_playable(self.hand_card[it],
                                                                                                   card_color,
                                                                                                   card_played,
                                                                                                   get_teammate[it])))

                    def check(inter_choose_card):
                        b_id = inter_choose_card.clicked_button.custom_id.split("-")
                        if inter_choose_card.message.id == msgs[it].id and self.players[it] == inter_choose_card.author:
                            card_played[it] = belote_card.Card(c_id_to_c[b_id[0]], int(b_id[1]), belote_card.get_trump_color(self.id))
                            c_player_hand = self.hand_card[it]
                            d_n = None
                            for c in range(len(c_player_hand)):
                                if str(c_player_hand[c]) == inter_choose_card.clicked_button.custom_id:
                                    d_n = c
                            del self.hand_card[it][d_n]
                            card_played[str(belote_card.Card(c_id_to_c[b_id[0]],
                                                             int(b_id[1]),
                                                             belote_card.get_trump_color(self.id)))] = it
                            return True
                        return False

                    inter = await msgs[it].wait_for_button_click(check)
                    if len(self.hand_card[it]) != 0:
                        await msgs[it].edit(components=belote_card.to_buttons(self.hand_card[it], []))
                    else:
                        await msgs[it].edit(components=[])
                    if card_color is None:
                        card_color = c_id_to_c[inter.clicked_button.custom_id.split("-")[0]]
                    await inter.reply(content="c", type=6)
                p_win = card_played[str(belote_card.beats(card_color, list(card_played.values())))]
                next_player_to_play = p_win
                f_card_list = []
                for ite in self.players:
                    await msgs[ite].edit(embed=get_game_message(embed, card_played, ite))
                await asyncio.sleep(0.5)
                for ca in list(card_played.values()):
                    if type(ca) is belote_card.Card:
                        f_card_list.append(ca)
                self.cards += f_card_list
                self.teams_score["current"][player_to_team[p_win]] += belote_card.get_points(list(card_played.values()))
            # calculate point
            self.teams_score["current"][player_to_team[next_player_to_play]] += 10
            if self.teams_score["current"][player_to_team[who_take_trump]] < self.teams_score["current"][
                player_to_team[
                    get_next[who_take_trump]]]:
                self.teams_score["current"][player_to_team[who_take_trump]] = 0
                self.teams_score["current"][player_to_team[get_next[who_take_trump]]] = 162
            elif self.teams_score["current"][player_to_team[who_take_trump]] == 162:
                self.teams_score["current"][player_to_team[who_take_trump]] = 252
            self.teams_score["global"]["ns"] += self.teams_score["current"]["ns"]
            self.teams_score["current"]["ns"] = 0
            self.teams_score["global"]["eo"] += self.teams_score["current"]["eo"]
            self.teams_score["current"]["eo"] = 0
            # cut the game
            cut_int = random.randint(5, 27)
            self.cards = self.cards[cut_int:32] + self.cards[0:cut_int]
            start_player = get_next[start_player]
            # give it to players
            self.distribute(3)
            self.distribute(2)
            # update score embed
            embed = self.update_score(embed, self.teams_score)
            await edits(msgs, embed=embed)

        # remove tmp game channel
        for msg in msgs.values():
            await msg.channel.delete()

        # send win message
        win_embed = discord.Embed(color=0x37ff00)
        win_embed.add_field(name="Victoire",
                            value="ㅤ\nVictoire de l'équipe " +
                                  ("NS " + self.players["n"].mention + " " + self.players["s"].mention
                                   if self.teams_score["global"]["ns"] > self.teams_score["global"]["eo"] else
                                   "EO " + self.players["e"].mention + self.players["o"].mention) +
                                  "\nㅤNS : " + str(self.teams_score["global"]["ns"]) +
                                  "\nㅤEO " + str(self.teams_score["global"]["eo"])
                            )
        await self.j_msg.edit(embed=win_embed)
        belote_card.del_trump_color(self.id)
        del ids[self.id]

    # the function to distribute card to player
    def distribute(self, card_n, player=None):
        if player is None:
            for i in self.players:
                self.hand_card[i] += self.cards[0:card_n]
                del self.cards[0:card_n]
        else:
            self.hand_card[player] += self.cards[0:card_n]
            del self.cards[0:card_n]

    # the function ton update the score in the embed
    def update_score(self, embed, score):
        embed.set_field_at(index=2,
                           name="Scoreㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
                           value="ㅤ\ncurrent\nNS (" + self.players["n"].name + ", " + self.players["s"].name +
                                 ") : " + str(score["current"]["ns"]) +
                                 "\nEO (" + self.players["e"].name + ", " + self.players["o"].name +
                                 ") : " + str(score["current"]["eo"]) +
                                 "ㅤ\ntotal\nNS (" + self.players["n"].name + ", " + self.players["s"].name +
                                 ") : " + str(score["global"]["ns"]) +
                                 "\nEO (" + self.players["e"].name + ", " + self.players["o"].name +
                                 ") : " + str(score["global"]["eo"]) +
                                 "\n\n**Atout** : " + belote_card.get_trump_color(self.id).value["emoji"] + "\n",
                           inline=True)
        return embed

    # make a list with all the card
    def make_cards_list(self):
        t_cards = [[belote_card.Card(i, m, belote_card.get_trump_color(self.id)) for m in range(7, 14)] for i in [
            belote_card.Color.COEUR,
            belote_card.Color.TREFLE,
            belote_card.Color.CARREAUX,
            belote_card.Color.PIQUE]]
        self.cards = []
        for i in t_cards:
            self.cards += i
        for i in [belote_card.Color.COEUR,
                  belote_card.Color.TREFLE,
                  belote_card.Color.CARREAUX,
                  belote_card.Color.PIQUE]:
            self.cards.append(belote_card.Card(i, 1, belote_card.get_trump_color(self.id)))

        random.shuffle(self.cards)


# function for edit multiple message
async def edits(msgs, **kwargs):
    for msg in msgs.values():
        await msg.edit(**kwargs)


# create a list who start to a player and do a circle
def start_player_to_play_list(f_p, s=None, r_list=None):
    if r_list is None:
        r_list = []
    if f_p == s:
        return r_list
    else:
        r_list.append(f_p)
        if s is None:
            return start_player_to_play_list(get_next[f_p], f_p, r_list)
        else:
            return start_player_to_play_list(get_next[f_p], s, r_list)
