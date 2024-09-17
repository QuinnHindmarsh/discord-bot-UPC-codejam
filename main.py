from discord import Intents, Client, Message, utils
from private import token
from responses import get_response
from copy import deepcopy

# bot setup
intents: Intents = Intents.default()
intents.message_content = True  # NQQA
intents.members = True  # NQQA

client: Client = Client(intents=intents)

# adds role to mentioned member


async def add_role(message: Message, roleName='member'):
    UID = str(deepcopy(message.content))
    UID = UID.replace('!member ', '')
    UID = UID.replace('<@', '')
    UID = UID.replace('>', '')
    UID = int(UID)

    role = utils.get(message.guild.roles, name=roleName)
    target_member = utils.get(client.get_all_members(), id=UID)

    await target_member.add_roles(role)
    return f'Role has been succsesfully added to {target_member.name}'

# finds the appropraite function to call based on the message content


async def get_response(message: Message):
    message_content = message.content
    if message_content[0] != '!':
        return False

    if message_content.startswith('!member'):
        return await add_role(message)


# deals with recived messages
async def send_message(message: Message) -> None:
    message_content = message.content

    if not message_content:
        print('user message is empty')
        return

    response: str = await get_response(message)
    if response != False:
        await message.channel.send(response)

"""
    try:
        response: str = get_response(message)
        if response != False:
            await message.channel.send(response)

    except Exception as e:
        print(e)
"""

# called on startup


@client.event
async def on_ready():
    print(f'{client.user} is now running')


# called when message is sent
@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    await send_message(message)


#  Runs bot
def main():
    client.run(token=token)


main()
