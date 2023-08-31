import json
import pprint


class Spell:
    def __init__(self, data):
        self.spell_name = data["mScriptName"]
        self.data_values = data["mSpell"]["mDataValues"]
        self.spell_calculations = data["mSpell"]["mSpellCalculations"]

    def compute_formula_from_parts(self, formula_parts):
        for part in formula_parts:
            print(part)
            print(part["__type"])
            print(part["mDataValue"])

    def compute_spell_computations(self):
        for calc in self.spell_calculations.keys():
            if self.spell_calculations[calc]["__type"] == "GameCalculation":
                formula_parts = self.spell_calculations[calc]["mFormulaParts"]
                self.compute_formula_from_parts(formula_parts)
