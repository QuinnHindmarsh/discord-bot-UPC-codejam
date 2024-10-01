from discord import Intents, Client, Message, utils, Member
import discord
from datetime import datetime

from commands import Commands


class Control:
    def __init__(self, client: Client, commands: Commands):
        self.__client = client
        self.__commands = commands

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
        message_content = message.content.lower()
        if self.__commands.inConvo == True and message.author.id == self.__commands.currentUserID:
            return await self.__commands.currentFunc(message)

        elif message_content[0] != '!':
            return False
        elif message_content.startswith('!member'):
            return await self.__commands.add_role(message)
        elif message_content.startswith('!spam'):
            return await self.__commands.renew(message)
        elif message_content.startswith('!msgnonmembers'):
            return await self.__commands.msg_non_members(message)
        elif message_content.startswith('!help'):
            return await self.__commands.help()
        elif message_content.startswith('!set event'):
            return await self.__commands.set_event(message)
        elif message_content.startswith('!see events'):
            return await self.__commands.display_events()
        elif message_content.startswith('!del event'):
            return await self.__commands.delete_event(message)
