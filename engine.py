import tdl

def main():
    screen_width = 80
    screen_height = 50

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(screen_width, screen_height, title='Roguelike Tutorial Revised')

    while not tdl.event.is_window_closed():
        root_console.draw_char(1, 1, '@', bg=None, fg=(255, 255, 255))
        tdl.flush()

        root_console.draw_char(1, 1, ' ', bg=None)

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue

        if user_input.key == 'ESCAPE':
            return True

if __name__ == '__main__':
    main()
