import asyncio
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
                custom_id="4",
                emoji="4️⃣"
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="7",
                emoji="7️⃣"
            )
        ), ActionRow(
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
                custom_id="6",
                emoji="6️⃣"
            )
        ), ActionRow(
            Button(
                style=ButtonStyle.gray,
                custom_id="d1",
                emoji="⚫",
                disabled=True
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="5",
                emoji="5️⃣"
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id="d2",
                emoji="⚫",
                disabled=True
            )
        )]

    async def start(self):
        while True:
            self.update_board()
            await self.ctx.edit(embed=self.get_board_embed(), components=self.buttons)

            def check(inter):
                return inter.message.id == self.ctx.id and \
                       len(self.board[int(inter.clicked_button.custom_id)-1]) < 6

            inter = await self.ctx.wait_for_button_click(check)
            await inter.reply("c", type=6)
            m_color = int_to_state[self.c_player + 1]
            x = int(inter.clicked_button.custom_id) - 1
            y = len(self.board[x])
            self.board[x].append(m_color)

            for xy in [(1, 1), (1, -1), (1, 0), (0, 1)]:
                c_count = 1
                i = 1
                while True:
                    if m_color != self.get_color(i * xy[0] + x, i * xy[1] + y):
                        break
                    else:
                        c_count += 1
                    i += 1

                i = -1
                while True:
                    if m_color != self.get_color(i * xy[0] + x, i * xy[1] + y):
                        break
                    else:
                        c_count += 1
                    i -= 1

                if c_count >= 4:
                    self.update_board()
                    await self.ctx.edit(content="ㅤ"
                                        , components=[],
                                        embed=self.get_board_embed())
                    await asyncio.sleep(.5)
                    embed = discord.Embed(title="Victory", color=0x37ff00)
                    embed.add_field(name="ㅤ", value="Victoire de " +
                                                    self.players[self.c_player].mention + " (" +
                                                    int_to_emoji[self.c_player+1] + ")" +
                                                    " Victoire")
                    embed.set_footer(text="This game was made by Jnath#5924")
                    await self.ctx.edit(content="", embed=embed, components=[])
                    return

            draw = True
            for i in self.board.values():
                if len(i) < 6:
                    draw = False
                    break

            if draw:
                self.update_board()
                await self.ctx.edit(content="ㅤ"
                                    , components=[],
                                    embed=self.get_board_embed())
                await asyncio.sleep(.5)
                embed = discord.Embed(title="Égalité", color=0xff0000)
                embed.add_field(name="ㅤ",
                                value=self.players[0].mention + " à fait une égalité avec" + self.players[1].mention)
                embed.set_footer(text="This game was made by Jnath#5924")
                await self.ctx.edit(components=[], embed=embed)
                return

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

        embed.add_field(name="ㅤ" + int_to_emoji[self.c_player + 1] + " " +
                             self.players[self.c_player].name,
                        value="\n".join(list(reversed(self.b_board)) +
                                        [":one: | :two: | :three: | :four: | :five: | :six: | :seven:"]))
        embed.set_footer(text="This game was made by Jnath#5924")
        return embed

    def get_color(self, x, y):
        if 0 <= x < 7 and 0 <= y < len(self.board[x]):
            return self.board[x][y]
        return State.NOTHING
