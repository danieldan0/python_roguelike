from enum import Enum
import textwrap
import tdl


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def get_entities_under_mouse(mouse_coordinates, entities, game_map):
    """
    Used for displaying info when entities are hovered.

    :param mouse_coordinates: tuple<int>(x, y)
    :param entities: list<Entity>
    :param game_map: GameMap
    :return: list<Entity>
    """
    x, y = mouse_coordinates

    entities_under_mouse = [entity for entity in entities
                            if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]

    return entities_under_mouse


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    """
    Render a bar (HP, experience, etc).

    :param panel: tdl.Console
    :param x: int
    :param y: int
    :param total_width: int
    :param name: string
    :param value: int
    :param maximum: int
    :param bar_color: tuple<int>(r, g, b)
    :param back_color: tuple<int>(r, g, b)
    :param string_color: tuple<int>(r, g, b)
    """

    # first calculate the width of the bar

    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with the values
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)


def menu(con, header, options, width, screen_height, screen_width, colors, mouse_coordinates=(0, 0)):
    """
    Renders a menu(inventory, shop etc). Returns a clicked option.

    :param con: tdl.Console
    :param header: string
    :param options: array
    :param width: int
    :param screen_height: int
    :param screen_width: int
    :param colors: dict<tuple<int>(r, g, b)>
    :param mouse_coordinates: tuple<int>(x, y)
    :return: int/None
    """
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after textwrap) and one line per option
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tdl.Console(width, height)

    # print the header, with wrapped text
    window.draw_rect(0, 0, width, height, None, fg=colors.get("white"), bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.draw_str(0, y, text, bg=None)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    con.blit(window, x, y, width, height, 0, 0)

    # compute x and y offsets to convert console position to menu position
    x_offset = x  # x is the left edge of the menu
    y_offset = y + header_height  # subtract the height of the header from the top edge of the menu

    while True:
        # present the root console to the player and check for input
        tdl.flush()
        user_input = None
        button = None
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
            if event.type == 'MOUSEDOWN':
                button = event.button
                mouse_coordinates = event.cell
            if event.type == 'MOUSEMOTION':
                button = None
                mouse_coordinates = event.cell
        else:
            user_input = None
            button = None

        letter_index = ord('a')
        for option_text in options:
            text = '(' + chr(letter_index) + ') ' + option_text
            menu_y = mouse_coordinates[1] - y_offset
            if menu_y == mouse_coordinates[0]:
                bg = colors.get("white")
            else:
                bg = None

            window.draw_str(0, y, text, bg=bg)
            y += 1
            letter_index += 1

        if button == "LEFT":
            menu_x, menu_y = (mouse_coordinates[0] - x_offset, mouse_coordinates[1] - y_offset)
            # check if click is within the menu and on a choice
            if width > menu_x >= 0 and height - header_height > menu_y >= 0:
                return menu_y
            else:
                return None

        if user_input.key == 'ENTER' and user_input.alt:
            tdl.set_fullscreen(not tdl.get_fullscreen())


def render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log, screen_width,
               screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors):
    """
    Renders all.

    :param con: tdl.Console
    :param panel: tdl.Console
    :param entities: list<Entity>
    :param player: Entity
    :param game_map: GameMap
    :param fov_recompute: bool
    :param root_console: tdl.Console
    :param message_log: MessageLog
    :param screen_width: int
    :param screen_height: int
    :param bar_width: int
    :param panel_height: int
    :param panel_y: int
    :param mouse_coordinates: tuple(x, y)
    :param colors: dict<tuple<int>(r, g, b)>
    """
    if fov_recompute:
        for x, y in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('light_ground'))
                game_map.explored[x][y] = True
            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get('dark_ground'))

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map.fov)

    root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)

    panel.clear(fg=colors.get('white'), bg=colors.get('black'))

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        panel.draw_str(message_log.x, y, message.text, bg=None, fg=message.color)
        y += 1

    entities_under_mouse = get_entities_under_mouse(mouse_coordinates, entities, game_map)

    render_bar(panel, 1, 0, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               colors.get('light_red'), colors.get('darker_red'), colors.get('white'))

    y = 1

    for entity in entities_under_mouse:
        panel.draw_str(1, y, entity.name)
        if entity.render_order == RenderOrder.ACTOR:
            render_bar(panel, len(entity.name) + 1, y, bar_width, 'HP', entity.fighter.hp,
                       player.fighter.max_hp, colors.get('light_red'), colors.get('darker_red'), colors.get('white'))
        y += 1

    root_console.blit(panel, 0, panel_y, screen_width, panel_height, 0, 0)


def clear_all(con, entities):
    """
    Clears all entities.

    :param con: tdl.Console
    :param entities: list<Entity>
    """
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov):
    """
    Draws entity.

    :param con: tdl.Console
    :param entity: Entity
    :param fov: tdl.Map.fov
    """
    if fov[entity.x, entity.y]:
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)


def clear_entity(con, entity):
    """
    Erases the character that represents entity.

    :param con: tdl.Console
    :param entity: Entity
    """
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
