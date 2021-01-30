class HooNewsMessage:
    def __init__(self, chat_id, message_type, content):
        self.chat_id = chat_id
        self.message_type = message_type
        self.content = content

    def __repr__(self):
        return f"message_type: {self.message_type}, contet: {self.content}"
