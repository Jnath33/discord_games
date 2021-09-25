from enum import Enum
from filecmp import cmp


class Color(Enum):
    COEUR = {"id": "co", "emoji": (":heart:", "❤️️"), "int": 1}
    CARREAUX = {"id": "ca", "emoji": (":diamonds:", "♦️"), "int": 2}
    TREFLE = {"id": "tr", "emoji": (":clubs:", "♣️"), "int": 3}
    PIQUE = {"id": "pi", "emoji": (":spades:", "♠️"), "int": 4}


to_atout = {7: 1, 8: 2, 12: 3, 13: 4, 10: 5, 1: 6, 9: 7, 11: 8}
to_normal = {7: 1, 8: 2, 9: 3, 11: 4, 12: 5, 13: 6, 10: 7, 1: 8}
atout_color = None
nomber_to_name = {7:"7",8:"8",9:"9",10:"10",11:"Valet",12:"Dame",13:"Roi",1:"As"}


def to_buttons(card_list):
    card_list.sort()
    for card in card_list:
        print(str(card))



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
        return cmp((self.color.value["int"]*100 + self.nomber), (other.color.value["int"]*100+other.nomber))

    def __eq__(self, other):
        return (self.color.value["int"]*100 + self.nomber) == (other.color.value["int"]*100+other.nomber)

    def __ne__(self, other):
        return (self.color.value["int"]*100 + self.nomber) != (other.color.value["int"]*100+other.nomber)

    def __lt__(self, other):
        return (self.color.value["int"]*100 + self.nomber) < (other.color.value["int"]*100+other.nomber)

    def __le__(self, other):
        return (self.color.value["int"]*100 + self.nomber) <= (other.color.value["int"]*100+other.nomber)

    def __gt__(self, other):
        return (self.color.value["int"]*100 + self.nomber) > (other.color.value["int"]*100+other.nomber)

    def __ge__(self, other):
        return (self.color.value["int"]*100 + self.nomber) >= (other.color.value["int"]*100+other.nomber)

    def __str__(self):
        return self.color.value["id"]+" "+nomber_to_name[self.nomber]


def beats(color_start, cards):
    c_best = cards[0]
    for i in range(3):
        if not c_best.beat(color_start, i):
            c_best = i
    return c_best