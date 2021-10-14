import json
from enum import Enum
from ordered_enum import OrderedEnum


def lg_t(*args, **kwargs):
    pass


def sv_t(*args, **kwargs):
    pass


def sorciere_t(*args, **kwargs):
    pass


def ancien_t(*args, **kwargs):
    pass


def voyante_t(*args, **kwargs):
    pass


# global variable
to_privacy = {}
name_to_role = {}


class Role(OrderedEnum):
    # Role dict data :
    #
    # {
    #   "name": name
    #   "audio": audio_folder_name
    #   "func":
    #   {
    #     "game": turn_func
    #     "death": death_func
    #     "start": start_func
    #   }
    # }
    #
    #
    LG = \
        {
            "name": "Loup-Garou",
            "audio": "LG",
            "func":
                {
                    "game": lg_t,
                    "death": None,
                    "start": None
                }
        }
    SV = {"name": "t"}

    @staticmethod
    def get_from_name(name):
        try:
            return name_to_role[name]
        except KeyError:
            return Role.SV


class Settings:
    # Json Format :
    #
    # {
    #   "name": name of the game,
    #   "roles": list of roles in the game,
    #   "privacy": 1, 2 or 3 refert u on the privacy
    #   "vocal": True or False for know if the game are played in vocal
    # }
    #
    #

    class Privacy(Enum):
        PUBLIC = (False, False, 1)  # The game is accesible for everybody
        PRIVATE = (False, True, 2)  # The game need a code to join it
        PROTECTED = (True, True, 3)  # The game need a code and a password to join it

        @staticmethod
        def get(n):
            try:
                return to_privacy[n]
            except KeyError:
                return Settings.Privacy.PRIVATE

    def __init__(self, from_json=None):
        if from_json is None:
            self.name = "PartieSansNom"
            self.roles = []
            self.vocal = False
            self.privacy = Settings.Privacy.PRIVATE
        else:
            self.name = from_json["name"]
            self.roles = from_json["roles"]
            self.vocal = from_json["vocal"]
            self.privacy = from_json["privacy"]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "roles": self.roles,
            "vocal": self.vocal,
            "privacy": self.privacy[2]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(),
                          separators=(',', ':'))


# set the variables
for i in Role:
    name_to_role[i.name] = i
    name_to_role[i.value["name"]] = i

for i in Settings.Privacy:
    to_privacy[i.value[2]] = i
    to_privacy[i.name] = i

t = [Role.SV, Role.LG, Role.SV, Role.LG]

t.sort(
)

for i in t:
    print(i.value)
