import math

from render_functions import RenderOrder


class Entity:
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None):
        """
        Entity class.

        :param x: int
        :param y: int
        :param char: string
        :param color: tuple<int>(r, g, b)
        :param name: string
        :param blocks: bool
        :param render_order: RenderOrder
        :param fighter: class
        :param ai: class
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.components = []
        self.fighter = fighter
        self.ai = ai
        self.item = item

        # let the components know who owns it
        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

    def has_component(self, component):
        """
        Returns True if entity has component.

        :param component: class
        :return: bool
        """
        return component.name in self.components

    def move(self, dx, dy):
        """
        Move the entity by a given amount

        :param dx: int
        :param dy: int
        """
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        """
        Move the entity towards target.

        :param target_x: int
        :param target_y: int
        :param game_map: GameMap
        :param entities: list<Entity>
        """
        path = game_map.compute_path(self.x, self.y, target_x, target_y)

        dx = path[0][0] - self.x
        dy = path[0][1] - self.y

        if game_map.walkable[path[1][0], path[1][1]] and \
                not get_blocking_entities_at_location(entities, self.x + dx, self.y + dy):
            self.move(dx, dy)

    def distance_to(self, other):
        """
        Returns the distance to another object.

        :param other: Entity
        :return: float
        """
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """
    Gets blocking entities at location. Returns None if no entities were found.

    :param entities: list<Entity>
    :param destination_x: int
    :param destination_y: int
    :return: Entity/None
    """
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
