from enum import Enum
from filecmp import cmp
from dislash import ButtonStyle, Button, ActionRow


# color class the color of a card (Carreaux, coeur, trefle, pique)
class Color(Enum):
    COEUR = {"id": "co", "emoji": ":heart:", "uemoji": "❤️", "int": 1}
    CARREAUX = {"id": "ca", "emoji": ":diamonds:", "uemoji": "♦️", "int": 2}
    TREFLE = {"id": "tr", "emoji": "`♣️`", "uemoji": "♣️", "int": 3}
    PIQUE = {"id": "pi", "emoji": "`♠️`", "uemoji": "♠️", "int": 4}
    VOID = {"id": "void", "emoji": ":no_entry_sign:", "uemoji": "🚫", "int": 0}


# dictionary
to_trump = {7: 1, 8: 2, 12: 3, 13: 4, 10: 5, 1: 6, 9: 7, 11: 8}
to_normal = {7: 1, 8: 2, 9: 3, 11: 4, 12: 5, 13: 6, 10: 7, 1: 8}
trump_point = {7: 0, 8: 0, 9: 14, 10: 10, 11: 20, 12: 3, 13: 4, 1: 11}
normal_point = {7: 0, 8: 0, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4, 1: 11}
trump_color = {}
nomber_to_name = {7: "7", 8: "8", 9: "9", 10: "10", 11: "Valet", 12: "Dame", 13: "Roi", 1: "As"}


# function for trump
def get_trump_color(g_id):
    if not g_id in trump_color:
        trump_color[g_id] = Color.VOID
    return trump_color[g_id]


def set_trump_color(g_id, color):
    trump_color[g_id] = color


def del_trump_color(g_id):
    del trump_color[g_id]


# Function for transform the card in hand of the player to the button list whi the
# authorized_button are the button are enabled
def to_buttons(card_list, authorized_button):
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
    raw = []
    for i in range(int((len(card_buttons) - 1) / 5) + 1):
        raw.append(ActionRow(*card_buttons[i * 5:min((i + 1) * 5, len(card_buttons))]))
        for it in range(min((i + 1) * 5, len(card_buttons) - i * 5)):
            if raw[i].components[it].custom_id in authorized_button:
                raw[i].enable_buttons(it)

    return raw


# return a list of authorized_button
def get_playable(card_list, color, card_played, team_mate):
    all_card = False
    cards = []
    cards_nv = list(card_played.values())
    for card in cards_nv:
        if type(card) is Card:
            if card.color == trump_color:
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
                if card.color == card.trump_color:
                    can_play.append(card)
                    if team_mate in card_played and str(beats(color, list(card_played.values()))) == str(
                            card_played[team_mate]):
                        all_card = True
        n_can_play = []
        if b_att is not None:
            for card in can_play:
                if card > b_att:
                    n_can_play.append(card)
        if len(n_can_play) != 0:
            can_play = n_can_play
    if len(can_play) == 0 or all_card:
        can_play = []
        for card in card_list:
            can_play.append(card)
    return [str(i) for i in can_play]


# Card class
class Card:
    def __init__(self, color: Color, number: int, trump_color):
        self.color = color
        self.nomber = number
        self.trump_color = trump_color

    def beat(self, color_start, card):
        if self.color != card.color:
            if not color_start == card.color:
                if card.color == self.trump_color:
                    return True
                else:
                    return False
            else:
                if self.color == self.trump_color:
                    return False
                else:
                    return to_normal[self.nomber] < to_normal[self.nomber]
        c_list = to_trump if self.color == self.trump_color else to_normal
        return c_list[self.nomber] < c_list[card.nomber]

    def __cmp__(self, other):
        tpm_self = to_trump if self.color == self.trump_color else to_normal
        tpm_other = to_trump if other.color == self.trump_color else to_normal
        return cmp((self.color.value["int"] * 100 + tpm_self[self.nomber]),
                   (other.color.value["int"] * 100 + tpm_other[other.nomber]))

    def __eq__(self, other):
        tpm_self = to_trump if self.color == self.trump_color else to_normal
        tpm_other = to_trump if other.color == self.trump_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) == (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __ne__(self, other):
        tpm_self = to_trump if self.color == self.trump_color else to_normal
        tpm_other = to_trump if other.color == self.trump_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) != (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __lt__(self, other):
        tpm_self = to_trump if self.color == self.trump_color else to_normal
        tpm_other = to_trump if other.color == self.trump_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) < (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __le__(self, other):
        tpm_self = to_trump if self.color == self.trump_color else to_normal
        tpm_other = to_trump if other.color == self.trump_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) <= (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __gt__(self, other):
        tpm_self = to_trump if self.color == self.trump_color else to_normal
        tpm_other = to_trump if other.color == self.trump_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) > (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __ge__(self, other):
        tpm_self = to_trump if self.color == self.trump_color else to_normal
        tpm_other = to_trump if other.color == self.trump_color else to_normal
        return (self.color.value["int"] * 100 + tpm_self[self.nomber]) >= (
                other.color.value["int"] * 100 + tpm_other[other.nomber])

    def __str__(self):
        return self.color.value["id"] + "-" + str(self.nomber)


# function for know wath's card
def beats(color_start, cards_nv):
    cards = []
    for card in cards_nv:
        if type(card) is Card:
            cards.append(card)
    c_best = cards[0]
    for i in range(len(cards) - 1):
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
        if card.color == card.trump_color:
            point += trump_point[card.nomber]
        else:
            point += normal_point[card.nomber]
    return point
