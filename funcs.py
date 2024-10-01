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
        return sorted(unorderedDict, key=lambda item: datetime.strptime(unorderedDict[item], '%H:%M %d/%m/%y'))
        orderedDict = {}
        minDate = -1
        minKey = -1
        while len(orderedDict) != len(unorderedDict):
            print(1)
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

            print(minKey)
            if minKey != -1:
                if datetime.strptime(
                        unorderedDict[minKey], '%H:%M %d/%m/%y') > datetime.now():
                    orderedDict[minKey] = unorderedDict[minKey]
                del unorderedDict[minKey]
                minKey = -1
                minDate = -1
            else:
                print(f'output of sort events {orderedDict}')
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
            with open("events.json", 'r') as f:
                unorderedEvents = json.load(f)
        except FileNotFoundError:
            print('file not found error encountered')
            unorderedEvents = {}
        except json.decoder.JSONDecodeError:
            print('Json decode error encountered')
            unorderedEvents = {}

        return unorderedEvents

    def save_evet(self, name: str, time: datetime):
        unorderedEvents = self.load_json()
        print(f'this is the result from json load {unorderedEvents}')
        print(f'the file type loaded is {type(unorderedEvents)}')

        unorderedEvents[name] = time
        print(f'this the the dict about to be saved to JSON{unorderedEvents}')
        with open("events.json", 'w') as f:
            json.dump(unorderedEvents, f)
