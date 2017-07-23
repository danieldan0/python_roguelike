class BasicMonster:
    def take_turn(self, target, game_map, entities):
        """
        AI takes turn.

        :param target: Entity
        :param game_map: GameMap
        :param entities: list<Entity>
        :return: array
        """
        results = []

        monster = self.owner

        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
