from discord import Intents, Client, Message, utils, Member
import discord
from datetime import datetime

from funcs import Funcs


class Commands:
    def __init__(self, client: Client, funcs: Funcs):
        self.__client = client
        self.__funcs = funcs
        self.__inConvo = False
        self.__currentFunc = []

    # prints all commands

    async def help(self):
        commands = {
            '!member': 'Makes the mentioned person a member. exec role is neeeded to use this command',
            '!spam': 'Messages all members reminded them to renew membership. used in january. exec role is needed to use this command.',
            '!msgnonmembers': 'Messages all people in the discord who have not yet signed up (excluding industry, adelaide CSC execs) and have been in the discord for more then a week. exec role is needed to use this command.'

        }
        otherFuncions = [
            'When a user leaves a message is sent in #activity-log containg the users name and current member count.']

        txt = 'Commands:\n'
        for key in commands:
            txt += f'{key}: {commands[key]}\n'
        txt += '\nOther Functions:\n'
        for item in otherFuncions:
            txt += f'\u2022 {item}\n'

        return txt

    # adds role to mentioned member
    async def add_role(self, message: Message, roleName='member'):
        if await self.__funcs.check_for_role(message.author, 'exec') == True:
            role = utils.get(message.guild.roles, name=roleName)
            UID = self.__funcs.strip_UID(str(message.content))
            target_member = utils.get(self.__client.get_all_members(), id=UID)

            if await self.__funcs.check_for_role(target_member, 'member') == False:
                await target_member.add_roles(role)
                return f'Role has been succsesfully added to {target_member.name}.'
            else:
                return f'{target_member.name} already has member role.'
        else:
            return 'You can not apply member role to users as you are not a executive'

    # messages every member - used to remined people of renewal

    async def renew(self, message: Message):
        if await self.__funcs.check_for_role(message.author, 'exec') == False:
            return 'You can not use this command as you are not an executive.'
        if datetime.now().month != 1:
            return 'It is not January, you dont wanna message everyone yet'
        return 'remove this part to actually be able to send it'
        allUsers = self.__client.get_all_members()
        for user in allUsers:
            print(user.name)
            if user != self.__client.user and await self.__funcs.check_for_role(user, 'member') == True:
                channel = await user.create_dm()
                await channel.send('Hi,\nThis message has been automatically sent to all members to remined you that your membership to the UniSA Programming community automatically expires on the 1st of January. To continue to partipate in our events please renew it.\nThanks!\nhttps://usasa.sa.edu.au/clubs/join/7520/')
        return 'All members have been reminded of there expiring membership '

    # messages people who have been in the server for more then a week and dont have member or other relivent role to sign up

    async def msg_non_members(self, message: Message):
        if await self.__funcs.check_for_role(message.author, 'exec') == False:
            return 'You can not use this command as you are not an executive.'
        allUsers = self.__client.get_all_members()

        allUsersList = []
        for user in allUsers:
            allUsersList.append(user)

        nonMembers = []
        ignoredRoles = ['member', 'Adelaide CSC exec', 'Industry', 'exec']

        for user in allUsersList:
            flag = False
            for item in ignoredRoles:
                if await self.__funcs.check_for_role(user, item) == True:
                    flag = True
            if flag == False:
                if (datetime.now() - (user.joined_at.replace(tzinfo=None))).days >= 7:
                    nonMembers.append(user)

        # for user in nonMembers:
        #     if isinstance(user, Member):
        #         try:
        #             channel = await user.create_dm()
        #             await channel.send('Hi,\nyou have been in the UniSA Open Source Community discord for more then a week, and still have not signed up.\nIt only takes a minute to sign up, is free and you dont need to be a UniSA student to do it. Signing up is the best way to support our club and allow us to host as many future events as possible.\nhttps://usasa.sa.edu.au/clubs/join/7520/')
        #         except discord.errors.HTTPException:
        #             print(f'{user.name} could not be messaged')

        return f'{[x.name for x in nonMembers]} have all been direct messaged. - not actually code is commented out'

    async def set_event(self, message: Message):
        # datetime_object = datetime.strptime(datetime_str, '%H:%M %d/%m/%y')
        if message.content.startswith('!set event'):
            self.__inConvo = True
            self.__step = 1
            self.__currentFunc[0] = self.set_event
            return 'enter event date/time (h:m dd/m/yy).'
        if self.__step == 1:
            try:
                self.__eventInMemoryTime = datetime.strptime(
                    message.content, '%H:%M %d/%m/%y')
                print(type(self.__eventInMemoryTime))
                self.__step = 2
                return f'Time is set at {self.__eventInMemoryTime}. Please enter the name of the event.'
            except:
                return f'Time was not entered correctly, please enter to the format h:m dd/m/yy.'
        if self.__step == 2:
            self.__eventInMemoryName = message.content
            return f'Event has been saved in memory as {self.__eventInMemoryName}.'

    def get_inConvo(self):
        return self.__inConvo

    def get_currentFunc(self):
        return self.__currentFunc

    inConvo = property(get_inConvo)
    currentFunc = property(get_currentFunc)
