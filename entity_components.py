class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    name = "fighter"
    def __init__(self, properties):
        self.damage = properties["damage"]

class Destructible:
    #taking damage
    name = "destructible"
    def __init__(self, properties):
        self.max_hp = properties["max_hp"]
        self.hp = properties["hp"]
        self.defense = properties["defense"]

    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
