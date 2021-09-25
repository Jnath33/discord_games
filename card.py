from enum import Enum


class Color(Enum):
    COEUR = {"id": "co", "emoji": (":heart:", "❤️️")}
    CARREAUX = {"id": "ca", "emoji": (":diamonds:", "♦️")}
    TREFLE = {"id": "tr", "emoji": (":clubs:", "♣️")}
    PIQUE = {"id": "pi", "emoji": (":spades:", "♠️")}


to_atout = {7: 1, 8: 2, 12: 3, 13: 4, 10: 5, 1: 6, 9: 7, 11: 8}
to_normal = {7: 1, 8: 2, 9: 3, 11: 4, 12: 5, 13: 6, 10: 7, 1: 8}
atout_color = None


def set_atout_color(color):
    atout_color = color


class Card:
    def __init__(self, color: Color, nomber: int, player: str):
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


def beats(color_start, cards):
    c_best = cards[0]
    for i in range(3):
        if not c_best.beat(color_start, i):
            c_best = i
    return c_best