from discord import Intents, Client, Message, utils, guild
from discord.ext.commands import context
from private import token
from responses import get_response
from copy import deepcopy

# bot setup
intents: Intents = Intents.default()
intents.message_content = True  # NQQA
intents.members = True  # NQQA

client: Client = Client(intents=intents)


def add_role(message: Message):
    UID = str(deepcopy(message.content))
    UID = UID.replace('!member ', '')
    UID = UID.replace('<@', '')
    UID = UID.replace('>', '')
    print(UID)
    return False


def get_response(message: Message):
    message_content = message.content
    if message_content[0] != '!':
        return False

    if message_content.startswith('!member'):
        return add_role(message)


async def send_message(message: Message) -> None:
    message_content = message.content

    if not message_content:
        print('user message is empty')
        return

    try:
        response: str = get_response(message)
        if response != False:
            await message.channel.send(response)

    except Exception as e:
        print(e)


# startup
@client.event
async def on_ready():
    print(f'{client.user} is now running')

# handling incoming messages


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    await send_message(message)


# main
def main():
    client.run(token=token)


main()
