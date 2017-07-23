from game_messages import Message


class Item:
    # an item that can be picked up and used.
    def pick_up(self, entities, inventory, colors):
        """
        Add to the player's inventory and remove from the map.

        :param entities: list<Entity>
        :param inventory: array
        :param colors: dict<tuple<int>(r, g, b)>
        :return: dict<Message>
        """
        if len(inventory) >= 26:
            return [{"message": Message('Your inventory is full, cannot pick up {0}.'.format(self.owner.name),
                                       colors.get("red"))}]
        else:
            inventory.append(self.owner)
            entities.remove(self.owner)
            return [{"message": Message('You picked up a {0}!'.format(self.owner.name), colors.get("green"))}]
