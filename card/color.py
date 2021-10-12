from enum import Enum


class Color(Enum):
    COEUR = {"id": "co", "emoji": ":heart:", "uemoji": "❤️", "int": 1}
    CARREAUX = {"id": "ca", "emoji": ":diamonds:", "uemoji": "♦️", "int": 2}
    TREFLE = {"id": "tr", "emoji": "`♣️`", "uemoji": "♣️", "int": 3}
    PIQUE = {"id": "pi", "emoji": "`♠️`", "uemoji": "♠️", "int": 4}
    VOID = {"id": "void", "emoji": ":no_entry_sign:", "uemoji": "🚫", "int": 0}


c_id_to_c = {
    "co": Color.COEUR,
    "ca": Color.CARREAUX,
    "tr": Color.TREFLE,
    "pi": Color.PIQUE,
    None: None
}
