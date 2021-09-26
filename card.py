from enum import Enum
from filecmp import cmp
from dislash import ButtonStyle, Button, ActionRow


class Color(Enum):
    COEUR = {"id": "co", "emoji": ":heart:", "uemoji": "❤️", "int": 1}
    CARREAUX = {"id": "ca", "emoji": ":diamonds:", "uemoji": "♦️", "int": 2}
    TREFLE = {"id": "tr", "emoji": ":clubs:", "uemoji": "♣️", "int": 3}
    PIQUE = {"id": "pi", "emoji": ":spades:", "uemoji": "♠️", "int": 4}


to_atout = {7: 1, 8: 2, 12: 3, 13: 4, 10: 5, 1: 6, 9: 7, 11: 8}
to_normal = {7: 1, 8: 2, 9: 3, 11: 4, 12: 5, 13: 6, 10: 7, 1: 8}
atout_point = {7: 0, 8: 0, 9: 14, 10: 10, 11: 20, 12: 3, 13: 4, 1: 11}
normal_point = {7: 0, 8: 0, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4, 1: 11}
atout_color = None
nomber_to_name = {7: "7", 8: "8", 9: "9", 10: "10", 11: "Valet", 12: "Dame", 13: "Roi", 1: "As"}


def to_buttons(card_list, autorized_button):
    card_list.sort()
    card_buttons = []
    for card in card_list:
        card_buttons.append(Button(
            style=ButtonStyle.gray,
            label=nomber_to_name[card.nomber],
            custom_id=str(card),
            emoji=card.color.value["uemoji"],
            disabled=True
        ))
    raws = []
    for i in range(int((len(card_buttons) - 1) / 5) + 1):
        raws.append(ActionRow(*card_buttons[i * 5:min((i + 1) * 5, len(card_buttons))]))
        for it in range(min((i + 1) * 5, len(card_buttons) - i * 5)):
            if raws[i].components[it].custom_id in autorized_button:
                raws[i].enable_buttons(it)

    return raws


def get_playable(card_list, color, cards_nv):
    cards = []
    for card in cards_nv:
        if type(card) is Card:
            if card.color == atout_color:
                cards.append(card)
    b_att = None
    for card in cards:
        if b_att is None:
            b_att = card
        else:
            if card > b_att:
                b_att = card
    can_play = []
    if color is not None:
        for card in card_list:
            if card.color == color:
                can_play.append(card)
        if len(can_play) == 0:
            for card in card_list:
                if card.color == atout_color:
                    can_play.append(card)
        n_can_play = []
        if b_att is not None:
            for card in can_play:
                if card > b_att:
                    n_can_play.append(card)
        if len(n_can_play) != 0:
            can_play = n_can_play
    if len(can_play) == 0:
        for card in card_list:
            can_play.append(card)
    return [str(i) for i in can_play]


class Card:
    def __init__(self, color: Color, nomber: int):
        self.color = color
        self.nomber = nomber

    def beat(self, color_start, card):
        if self.color != card.color:
            if not color_start == card.color:
                if card.color == atout_color:
                    return True
                else:
                    return False
            else:
                if self.color == atout_color:
                    return False
                else:
                    return to_normal[self.nomber] < to_normal[self.nomber]
        c_list = to_atout if self.color == atout_color else to_normal
        return c_list[self.nomber] < c_list[card.nomber]

    def __cmp__(self, other):
        tpm_self = to_atout if self.color == atout_color else to_normal
        tpm_other = to_atout if other.color == atout_color else to_normal
        return cmp((self.color.value["int"] * 100 + tpm_self[self.nomber]),
                   (other.color.value["int"] * 100 + tpm_other[other.nomber]))

    def __eq__(self, other):
        tpm_self = to_atout if self.color == atout_color else to_normal
        tpm_other = to_atout if other.color == atout_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) == (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __ne__(self, other):
        tpm_self = to_atout if self.color == atout_color else to_normal
        tpm_other = to_atout if other.color == atout_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) != (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __lt__(self, other):
        tpm_self = to_atout if self.color == atout_color else to_normal
        tpm_other = to_atout if other.color == atout_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) < (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __le__(self, other):
        tpm_self = to_atout if self.color == atout_color else to_normal
        tpm_other = to_atout if other.color == atout_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) <= (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __gt__(self, other):
        tpm_self = to_atout if self.color == atout_color else to_normal
        tpm_other = to_atout if other.color == atout_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) > (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __ge__(self, other):
        tpm_self = to_atout if self.color == atout_color else to_normal
        tpm_other = to_atout if other.color == atout_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) >= (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __str__(self):
        return self.color.value["id"] + "-" + str(self.nomber)


def beats(color_start, cards_nv):
    cards = []
    for card in cards_nv:
        if type(card) is Card:
            cards.append(card)
    c_best = cards[0]
    for i in range(3):
        if c_best.beat(color_start, cards[i + 1]):
            print(cards[i + 1])
            c_best = cards[i + 1]
    return c_best


def get_points(cards_nv):
    cards = []
    for card in cards_nv:
        if type(card) is Card:
            cards.append(card)
    point = 0
    for card in cards:
        if card.color == atout_color:
            point += atout_point[card.nomber]
        else:
            point += normal_point[card.nomber]
    return point
