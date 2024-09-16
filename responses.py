from discord import Message


def get_response(message: Message):
    message_content = message.content
    if message_content[0] != '!':
        return False

    if message_content.startswith('!member'):
        return 'test'
