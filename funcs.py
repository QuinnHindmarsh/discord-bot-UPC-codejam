from discord import Intents, Client, Message, utils, Member
import discord
from datetime import datetime


class Funcs:
    def __init__(self, client: Client):
        self.__client = client

    # check for specific role

    async def check_for_role(self, author, roleName):
        author_roles = author.roles
        flag = False
        for item in author_roles:
            if item.name == roleName:
                flag = True
        return flag

    # strips all text from userID+

    def strip_UID(self, text: str):
        textToRemove = ['!member ', '<@', '>']
        UID = text

        for item in textToRemove:
            UID = UID.replace(item, '')

        return int(UID)

    def save_evet(self, name: str, time: datetime):
        try:
            from events import Events
        except:
            Events = {}

        Events[name] = time

        f = open('discord-bot-UPC-codejam\\events.py', 'w')
        f.write(f'Events = {Events}')
        f.close()
