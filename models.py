class HooNewsMessage:
    def __init__(self, message_type, content):
        self.message_type = message_type
        self.content = content

    def __repr__(self):
        return f"message_type: {self.message_type}, contet: {self.content}"
