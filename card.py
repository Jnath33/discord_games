from enum import Enum
from filecmp import cmp
from dislash import ButtonStyle, Button, ActionRow


class Color(Enum):
    COEUR = {"id": "co", "emoji": ":heart:","uemoji": "❤️️", "int": 1}
    CARREAUX = {"id": "ca", "emoji": ":diamonds:","uemoji": "♦️", "int": 2}
    TREFLE = {"id": "tr", "emoji": ":clubs:","uemoji": "♣️", "int": 3}
    PIQUE = {"id": "pi", "emoji": ":spades:","uemoji": "♠️", "int": 4}


to_atout = {7: 1, 8: 2, 12: 3, 13: 4, 10: 5, 1: 6, 9: 7, 11: 8}
to_normal = {7: 1, 8: 2, 9: 3, 11: 4, 12: 5, 13: 6, 10: 7, 1: 8}
atout_color = None
nomber_to_name = {7: "7", 8: "8", 9: "9", 10: "10", 11: "Valet", 12: "Dame", 13: "Roi", 1: "As"}


def to_buttons(card_list, card_color=None):
    card_list.sort()
    card_buttons = []
    for card in card_list:
        card_buttons.append(Button(
            style=ButtonStyle.gray,
            label=nomber_to_name[card.nomber],
            custom_id=str(card),
            emoji=card.color.value["uemoji"],
        ))
    raws = []
    for i in range(int((len(card_buttons)-1)/5)-1):
        raws.append(ActionRow(*card_buttons[i*5:min((i+1)*5, len(card_buttons))]))
        if card_color is not None:
            for it in range(min((i+1)*5, len(card_buttons))):
                b = raws[i].components[it]
                if not b.custom_id.split("-")[0] in [card_color[id]]:
                    raws[i].disable_buttons(it)
                else:
                    raws[i].enable_buttons(it)

    return raws


def set_atout_color(color):
    atout_color = color


class Card:
    def __init__(self, color: Color, nomber: int, player):
        self.color = color
        self.nomber = nomber
        self.player = player

    def beat(self, color_start, card):
        if self.color != card.color:
            if not color_start == card.color:
                if card.color == atout_color:
                    return False
                else:
                    return True
            else:
                if card.color == atout_color:
                    return True
                else:
                    return False
        c_list = to_atout if self.color == atout_color else to_normal
        return c_list[self.nomber] > c_list[card.nomber]

    def __cmp__(self, other):
        return cmp((self.color.value["int"] * 100 + self.nomber), (other.color.value["int"] * 100 + other.nomber))

    def __eq__(self, other):
        return (self.color.value["int"] * 100 + self.nomber) == (other.color.value["int"] * 100 + other.nomber)

    def __ne__(self, other):
        return (self.color.value["int"] * 100 + self.nomber) != (other.color.value["int"] * 100 + other.nomber)

    def __lt__(self, other):
        return (self.color.value["int"] * 100 + self.nomber) < (other.color.value["int"] * 100 + other.nomber)

    def __le__(self, other):
        return (self.color.value["int"] * 100 + self.nomber) <= (other.color.value["int"] * 100 + other.nomber)

    def __gt__(self, other):
        return (self.color.value["int"] * 100 + self.nomber) > (other.color.value["int"] * 100 + other.nomber)

    def __ge__(self, other):
        return (self.color.value["int"] * 100 + self.nomber) >= (other.color.value["int"] * 100 + other.nomber)

    def __str__(self):
        return self.color.value["id"] + "-" + str(self.nomber)


def beats(color_start, cards):
    c_best = cards[0]
    for i in range(3):
        if not c_best.beat(color_start, i):
            c_best = i
    return c_best
