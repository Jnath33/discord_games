from filecmp import cmp

from dislash import ActionRow, Button, ButtonStyle

from card import color
from utils import menu


class Game:
    async def start(self, ctx):
        msg = await ctx.send(content="test", components=[])
        inter = await menu.new_menu(msg, Hand([Card(color.Color.COEUR, 1),
                                               Card(color.Color.COEUR, 2),
                                               Card(color.Color.COEUR, 3),
                                               Card(color.Color.COEUR, 4),
                                               Card(color.Color.COEUR, 5),
                                               Card(color.Color.COEUR, 6),
                                               Card(color.Color.COEUR, 7),
                                               Card(color.Color.COEUR, 8),
                                               Card(color.Color.COEUR, 9),
                                               Card(color.Color.TREFLE, 1),
                                               Card(color.Color.TREFLE, 2),
                                               Card(color.Color.TREFLE, 3),
                                               Card(color.Color.TREFLE, 4),
                                               Card(color.Color.TREFLE, 5),
                                               Card(color.Color.TREFLE, 8),
                                               Card(color.Color.TREFLE, 9),
                                               Card(color.Color.TREFLE, 10),
                                               Card(color.Color.TREFLE, 11),
                                               Card(color.Color.PIQUE, 1),
                                               Card(color.Color.PIQUE, 2),
                                               Card(color.Color.PIQUE, 4),
                                               Card(color.Color.PIQUE, 5),
                                               Card(color.Color.PIQUE, 9),
                                               Card(color.Color.PIQUE, 12),
                                               Card(color.Color.PIQUE, 3),
                                               Card(color.Color.PIQUE, 8),
                                               Card(color.Color.PIQUE, 6),
                                               Card(color.Color.CARREAUX, 1)]).get_buttons())
        print(inter.clicked_button.custom_id)


class Card:
    n_to_score = {1: 14, 2: 15, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13}

    def __init__(self, color, number):
        self.color = color
        self.number = number

    def can_play(self, count=1, played_card=None) -> bool:
        if played_card is None:
            return True
        else:
            if count >= played_card[0]:
                if played_card[1] >= 2:
                    if self.number == played_card[2]:
                        return True
                else:
                    if self.number >= played_card[2]:
                        return True
        return False

    def __cmp__(self, other):
        return cmp(Card.n_to_score[self.number], Card.n_to_score[other.number])

    def __eq__(self, other):
        return Card.n_to_score[self.number] == Card.n_to_score[other.number]

    def __ne__(self, other):
        return Card.n_to_score[self.number] != Card.n_to_score[other.number]

    def __lt__(self, other):
        return Card.n_to_score[self.number] < Card.n_to_score[other.number]

    def __le__(self, other):
        return Card.n_to_score[self.number] <= Card.n_to_score[other.number]

    def __gt__(self, other):
        return Card.n_to_score[self.number] > Card.n_to_score[other.number]

    def __ge__(self, other):
        return Card.n_to_score[self.number] >= Card.n_to_score[other.number]

    def __str__(self):
        return self.color.value["id"] + "-" + str(self.number)


class Hand:
    def __init__(self, hand=None):
        if hand is None:
            hand = []
        self.hand = hand

    def get_buttons(self, played_card=None,
                    disabled=False):  # played card is (n of card, superposition count, card nomber)
        self.hand.sort()
        buttons = [[ActionRow()]]
        c_buttons = 0
        c_list = 0
        for card in self.hand:
            buttons[c_list][c_buttons].add_button(
                style=ButtonStyle.gray,
                emoji=card.color.value["uemoji"],
                label=str(card.number),
                custom_id=str(card),
                disabled=(not card.can_play(self.hand.count(card), played_card)) or disabled
            )
            if len(buttons[c_list][c_buttons].buttons) == 5:
                c_buttons += 1
                if c_buttons == 4:
                    c_buttons -= 1
                    buttons.append([ActionRow()])
                    b = buttons[c_list][c_buttons].components[4]
                    del buttons[c_list][c_buttons].components[4]
                    buttons[c_list][c_buttons].add_button(
                        style=ButtonStyle.green,
                        label="=>",
                        custom_id=">",
                        disabled=disabled
                    )
                    c_buttons = 0
                    c_list += 1
                    buttons[c_list][c_buttons].add_button(
                        style=ButtonStyle.green,
                        label="<=",
                        custom_id="<",
                        disabled=disabled
                    )
                    buttons[c_list][c_buttons].components.append(b)
                else:
                    buttons[c_list].append(ActionRow())
        buttons[c_list][c_buttons].add_button(
            style=ButtonStyle.blurple,
            label="Pass",
            custom_id="pass",
            disabled=disabled
        )
        for i in buttons:
            t = 0
            for i_2 in i:
                t += len(i_2.components)
            print(t)
        if c_buttons == 4:
            c_buttons += -1
            buttons.append([ActionRow()])
            b = buttons[c_list][c_buttons].buttons[4]
            del buttons[c_list][c_buttons].buttons[4]
            buttons[c_list][c_buttons].add_button(
                style=ButtonStyle.green,
                label="=>",
                custom_id=">",
                disabled=disabled
            )
            c_buttons = 0
            c_list += 1
            buttons[c_list][c_buttons].add_button(
                style=ButtonStyle.green,
                label="<=",
                custom_id="<",
                disabled=disabled
            )
            buttons[c_list][c_buttons].buttons.append(b)
        return buttons
