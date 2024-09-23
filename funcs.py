from discord import Client
from datetime import datetime
import json


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

    def sort_events(self, unorderedDict):
        orderedDict = {}
        minDate = -1
        minKey = -1
        while len(orderedDict) != len(unorderedDict):
            for item in unorderedDict:

                if minDate == -1:
                    minDate = datetime.strptime(
                        unorderedDict[item], '%H:%M %d/%m/%y')
                    minKey = item
                elif minDate > datetime.strptime(
                        unorderedDict[item], '%H:%M %d/%m/%y'):
                    minDate = datetime.strptime(
                        unorderedDict[item], '%H:%M %d/%m/%y')
                    minKey = item

            if minKey != -1:
                if datetime.strptime(
                        unorderedDict[minKey], '%H:%M %d/%m/%y') > datetime.now():

                    orderedDict[minKey] = unorderedDict[minKey]
                del unorderedDict[minKey]
                minKey = -1
                minDate = -1
            else:
                return orderedDict

    # def save_evet(self, name: str, time: datetime):
    #     try:
    #         from events import Events
    #         orderedEvents = self.sort_events(Events)
    #     except ImportError:
    #         orderedEvents = {}

    #     orderedEvents[name] = time
    #     f = open('discord-bot-UPC-codejam\\events.py', 'w')
    #     f.write(f'Events = {orderedEvents}')
    #     f.close()

    def load_json(self):
        try:
            with open("discord-bot-UPC-codejam\\events.json", 'r') as f:
                unorderedEvents = json.load(f)
        except FileNotFoundError:
            unorderedEvents = {}
        except json.decoder.JSONDecodeError:
            unorderedEvents = {}

        return unorderedEvents

    def save_evet(self, name: str, time: datetime):
        unorderedEvents = self.load_json()

        unorderedEvents[name] = time
        orderedEvents = self.sort_events(unorderedEvents)
        print(orderedEvents)

        with open("discord-bot-UPC-codejam\\events.json", 'w') as f:
            json.dump(orderedEvents, f)
