from discord import Intents, Client, Message, utils, Member
import discord
from datetime import datetime

from private import token
from funcs import Funcs
from commands import Commands
from control import Control


# bot setup
intents: Intents = Intents.default()
intents.message_content = True  # NQQA
intents.members = True  # NQQA

client: Client = Client(intents=intents)

command = Commands(client)
funcs = Funcs(client)
control = Control(client)

# called on startup


@client.event
async def on_ready():
    print(f'{client.user} is now running')


# called when message is sent
@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    await control.send_message(message)


# send a message and member count each time user leaves server
@client.event
async def on_raw_member_remove(payload):
    print(payload)
    print(payload.user)

    channel = client.get_channel(1270268706349649940)
    memberCount = 0
    members = client.get_all_members()
    for member in members:
        memberCount += 1

    await channel.send(f'{payload.user} has now left, there are now {memberCount} members.')


#  Runs bot
def main():
    client.run(token=token)


main()
