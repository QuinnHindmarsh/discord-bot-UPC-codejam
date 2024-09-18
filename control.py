from discord import Intents, Client, Message, utils, Member
import discord
from datetime import datetime

from commands import Commands


class Control:
    def __init__(self, client):
        self.__commands = Commands(client)
        self.__client = client

    async def send_message(self, message: Message) -> None:
        message_content = message.content

        if not message_content:
            print('user message is empty')
            return

        response: str = await self.get_response(message)
        if response != False:
            await message.channel.send(response)

    # finds the appropraite function to call based on the message content
    async def get_response(self, message: Message):
        message_content = message.content
        if message_content[0] != '!':
            return False

        if message_content.startswith('!member'):
            return await self.__commands.add_role(message)
        elif message_content.startswith('!spam'):
            return await self.__commands.renew(message)
        elif message_content.startswith('!msgnonmembers'):
            return await self.__commands.msg_non_members(message)
        elif message_content.startswith('!help'):
            return await self.__commands.help()
