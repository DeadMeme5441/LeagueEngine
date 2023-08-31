import json
import pymongo
import pprint
from Spell import Spell


class Champion:
    def __init__(self, name):
        self.name = name

    @property
    def champ_data(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["league"]
        champ_data = mydb["base_data"].find_one({"champ_name": self.name})

        return champ_data

    @property
    def champ_abilities(self):
        abilities_path = "Characters/" + self.name + "/CharacterRecords/Root"

        abilities_list = self.champ_data["data"][abilities_path]["mAbilities"]

        abilities = []

        for ability in abilities_list:
            ability_dict = {}
            ability_dict["id"] = ability.split("/")[-1]
            ability_dict["path"] = "Characters/" + self.name + "/Abilities/" + ability

            abilities.append(ability_dict)

        return abilities

    def compute_spell(self, spell_path):
        spell = self.champ_data["data"][spell_path]

        spell_obj = Spell(spell)

        spell_obj.compute_spell_computations()

        return spell

    def compute_ability(self, ability_path):
        spells = self.champ_data["data"][ability_path]["mChildSpells"]

        spell = self.compute_spell(spells[0])

        return spell


if __name__ == "__main__":
    champ = Champion("Aatrox")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(champ.compute_ability("Characters/Aatrox/Spells/AatroxQAbility"))
    # pp.pprint(
    #     champ.calculate_ability_data("Characters/Aatrox/Abilities/AatroxQAbility/AatroxQ")
    # )
