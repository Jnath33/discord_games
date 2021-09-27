import asyncio
from enum import Enum
import random

import discord
from dislash import ActionRow, Button, ButtonStyle


class State(Enum):
    CIRCLE = 1
    CROSS = 2
    NOTHING = 0


int_to_emoji = {2: "❌", 1: "🟢", 0: "⚫"}
int_to_state = {2: State.CROSS, 1: State.CIRCLE, 0: State.NOTHING}


class Game:
    def __init__(self, ctx, players):
        self.board = {0: {0: State.NOTHING, 1: State.NOTHING, 2: State.NOTHING},
                      1: {0: State.NOTHING, 1: State.NOTHING, 2: State.NOTHING},
                      2: {0: State.NOTHING, 1: State.NOTHING, 2: State.NOTHING}}
        self.b_board = []
        self.update_buttons()
        self.ctx = ctx
        self.players = players
        self.c_player = random.randint(0, 1)

    def update_buttons(self):
        self.b_board = []
        for i in self.board:
            self.b_board.append(ActionRow(
                Button(
                    style=ButtonStyle.gray,
                    custom_id=str(i) + "-0",
                    emoji=int_to_emoji[self.board[i][0].value],
                    disabled=not self.board[i][0].value == 0
                ),
                Button(
                    style=ButtonStyle.gray,
                    custom_id=str(i) + "-1",
                    emoji=int_to_emoji[self.board[i][1].value],
                    disabled=not self.board[i][1].value == 0
                ),
                Button(
                    style=ButtonStyle.gray,
                    custom_id=str(i) + "-2",
                    emoji=int_to_emoji[self.board[i][2].value],
                    disabled=not self.board[i][2].value == 0
                )
            ))

    async def start(self):
        for i in range(9):
            self.update_buttons()
            await self.ctx.edit(content="ㅤ" +
                                        self.players[self.c_player].mention +
                                        " à ton tour (" +
                                        int_to_emoji[self.c_player + 1] + ")"
                                , components=self.b_board)

            def check(inter):
                return self.players[self.c_player] == inter.author and inter.message.id == self.ctx.id

            inter = await self.ctx.wait_for_button_click(check)
            await inter.reply(content='c', type=6)

            id = inter.clicked_button.custom_id.split("-")
            self.board[int(id[0])][int(id[1])] = int_to_state[self.c_player + 1]
            for i in [(0, 0, (1, 0)), (0, 1, (1, 0)), (0, 2, (1, 0)),
                      (0, 0, (0, 1)), (1, 0, (0, 1)), (2, 0, (0, 1)),
                      (0, 0, (1, 1)), (0, 2, (1, -1))]:
                if self.board[i[0]][i[1]] == \
                        self.board[i[0] + i[2][0]][i[1] + i[2][1]] == \
                        self.board[i[0] + i[2][0] * 2][i[1] + i[2][1] * 2] and \
                        self.board[i[0]][i[1]] != State.NOTHING:
                    embed = discord.Embed(title="Victory", color=0x37ff00)
                    embed.add_field(name="ㅤ", value="Victoire de " +
                                                    self.players[self.c_player].mention + " (" +
                                                    int_to_emoji[self.board[i[0]][i[1]].value] + ")" +
                                                    " Victoire")
                    embed.set_footer(text="This game was made by Jnath#5924")
                    await self.ctx.edit(content="", embed=embed, components=[])
                    return

            self.reverse_c_player()
        self.update_buttons()
        await self.ctx.edit(content="ㅤ"
                            , components=self.b_board)
        await asyncio.sleep(.5)
        embed = discord.Embed(title="Égalité", color=0xff0000)
        embed.add_field(name="ㅤ", value=self.players[0].mention + " à fait une égalité avec" + self.players[1].mention)
        embed.set_footer(text="This game was made by Jnath#5924")
        await self.ctx.edit(components=[], embed=embed)

    def reverse_c_player(self):
        self.c_player = 1 - self.c_player
