from discord import Intents, Client, Message, utils, Member
import discord
from datetime import datetime


class Funcs:
    def __init__(self, client):
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

    def strip_UID(self, text):
        textToRemove = ['!member ', '<@', '>']
        UID = text

        for item in textToRemove:
            UID = UID.replace(item, '')

        return int(UID)
