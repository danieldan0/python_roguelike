from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power):
        """
        Fighter class. Used for combat.

        :param hp: int
        :param defense: int
        :param power: int
        """
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        """
        Takes damage.

        :param amount: int
        :return: array<dict>
        """
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        """
        Attacks other entity.

        :param target: Entity
        :return: dict<Message>
        """
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name))})

        return results
