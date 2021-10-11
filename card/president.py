from dislash import ActionRow, Button, ButtonStyle

class Game:



class Card:
    n_to_score = {1:14,2:15,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13}
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def can_play(self, count = 1, played_card = None) -> bool:
        if played_card is None
            return True
        else:
            if count>=played_card[0]:
                if played_card[1]>=2:
                    if self.number == played_card[2]:
                        return True
                else:
                    if self.number >= played_card[2]:
                        return True
        return False

class Hand:
    def __init__(self, hand = []):
        self.hand = hand

    def get_buttons(self, played_card = None): # played card is (n of card, superposition count, card nomber)
        self.hand.sort()
        buttons =  [[ActionRow()]]
        c_buttons = 0
        c_list = 0
        for card in self.hand:
            buttons[c_list][c_buttons].add_button(
                style=ButtonStyle.gray,
                emoji=card.emoji,
                label=str(card.number),
                custom_id=str(card),
                disabled=not card.can_play(self.hand.count(card), played_card)
            )
            if len(buttons[c_list][c_buttons].buttons) == 5:
                c_buttons+=1
                if c_buttons == 5:
                    buttons.append([ActionRow()])
                    b = buttons[c_list][c_buttons].buttons[4]
                    del buttons[c_list][c_buttons].buttons[4]
                    buttons[c_list][c_buttons].add_button(
                        style=ButtonStyle.green,
                        label="=>",
                        custom_id=">"
                    )
                    c_buttons = 0
                    c_list += 1
                    buttons[c_list][c_buttons].add_button(
                        style=ButtonStyle.green,
                        label="<=",
                        custom_id="<"
                    )
                    buttons[c_list][c_buttons].buttons.append(b)
                else:
                    buttons[c_list].append(ActionRow())
        buttons[c_list][c_buttons].add_button(
            style=ButtonStyle.link,
            label="Pass",
            custom_id="pass"
        )
        if c_buttons == 5:
            buttons.append([ActionRow()])
            b = buttons[c_list][c_buttons].buttons[4]
            del buttons[c_list][c_buttons].buttons[4]
            buttons[c_list][c_buttons].add_button(
                style=ButtonStyle.green,
                label="=>",
                custom_id=">"
            )
            c_buttons = 0
            c_list += 1
            buttons[c_list][c_buttons].add_button(
                style=ButtonStyle.green,
                label="<=",
                custom_id="<"
            )
            buttons[c_list][c_buttons].buttons.append(b)
        return buttons
