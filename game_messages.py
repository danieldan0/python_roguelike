import textwrap


class Message:
    def __init__(self, text, color=(255, 255, 255)):
        """
        Colored string.

        :param text: string
        :param color: tuple<int>(r, g, b)
        """
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        """
        List of Messages.

        :param x: int
        :param width: int
        :param height: int
        """
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        """
        Adds message to MessageLog.

        :param message: Message
        """
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(message)
