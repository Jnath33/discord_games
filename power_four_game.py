from enum import Enum
import random

import discord
from dislash import ActionRow, Button, ButtonStyle


class State(Enum):
    YELLOW = 1
    RED = 2
    NOTHING = 0


int_to_emoji = {2: "🔴", 1: "🟡", 0: "⚫"}
int_to_state = {2: State.RED, 1: State.YELLOW, 0: State.NOTHING}


class Game:
    def __init__(self, ctx, players):
        self.board = {}
        for i in range(7):
            self.board[i] = []
        self.b_board = []
        self.update_board()
        self.ctx = ctx
        self.players = players
        self.c_player = random.randint(0, 1)
        self.buttons = [ActionRow(
            Button(
                style=ButtonStyle.gray,
                custom_id="1",
                emoji="1️⃣"
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="2",
                emoji="2️⃣"
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="3",
                emoji="3️⃣"
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="4",
                emoji="4️⃣"
            )
        ), ActionRow(
            Button(
                style=ButtonStyle.gray,
                custom_id="5",
                emoji="5️⃣"
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="6",
                emoji="6️⃣"
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="7",
                emoji="7️⃣"
            )
        )]

    async def start(self):
        while True:
            self.update_board()
            await self.ctx.edit(embed=self.get_board_embed(), components=self.buttons)

            def check(inter):
                return inter.message.id == self.ctx.id

            inter = await self.ctx.wait_for_button_click(check)
            await inter.reply("c", type=6)
            self.board[int(inter.clicked_button.custom_id) - 1].append(int_to_state[self.c_player + 1])
            self.c_player = 1 - self.c_player

    def get(self, x, y):
        if len(self.board[x]) > y:
            return self.board[x][y]
        return State.NOTHING

    def update_board(self):
        self.b_board = []
        for y in range(6):
            c_str = ""
            for x in range(7):
                c_str += int_to_emoji[self.get(x, y).value] + " | "
            self.b_board.append(c_str[0:-3])

    def get_board_embed(self):
        embed = discord.Embed(title="Waiting", color=0xfbff00)

        embed.add_field(name="ㅤ" + int_to_emoji[self.c_player+1]+ " " +
                             self.players[self.c_player].name,
                        value="\n".join(list(reversed(self.b_board)) +
                                        [":one: | :two: | :three: | :four: | :five: | :six: | :seven:"]))
        embed.set_footer(text="This game was made by Jnath#5924")
        return embed
