from discord import Intents, Client, Message, utils, Member
import discord
from private import token
from responses import get_response
from copy import deepcopy
from datetime import datetime

# bot setup
intents: Intents = Intents.default()
intents.message_content = True  # NQQA
intents.members = True  # NQQA

client: Client = Client(intents=intents)


# check for specific role
async def check_for_role(author, roleName):
    author_roles = author.roles
    flag = False
    for item in author_roles:
        if item.name == roleName:
            flag = True
    return flag


# strips all text from userID+
def strip_UID(text):
    textToRemove = ['!member ', '<@', '>']
    UID = text

    for item in textToRemove:
        UID = UID.replace(item, '')

    return int(UID)


# adds role to mentioned member


async def add_role(message: Message, roleName='member'):
    if await check_for_role(message.author, 'exec') == True:
        role = utils.get(message.guild.roles, name=roleName)
        UID = strip_UID(str(message.content))
        target_member = utils.get(client.get_all_members(), id=UID)

        if await check_for_role(target_member, 'member') == False:
            await target_member.add_roles(role)
            return f'Role has been succsesfully added to {target_member.name}.'
        else:
            return f'{target_member.name} already has member role.'
    else:
        return 'You can not apply member role to users as you are not a executive'


# messages every member - used to remined people of renewal
async def renew():
    if datetime.now().month != 1:
        return 'It is not January, you dont wanna message everyone yet'
    allUsers = client.get_all_members()
    for user in allUsers:
        print(user.name)
        if user != client.user and await check_for_role(user, 'member') == True:
            channel = await user.create_dm()
            await channel.send('Hi,\nThis message has been automatically sent to all members to remined you that your membership to the UniSA Programming community automatically expires on the 1st of January. To continue to partipate in our events please renew it.\nThanks!\nhttps://usasa.sa.edu.au/clubs/join/7520/')
    return 'All members have been reminded of there expiring membership '


# messages people who have been in the server for more then a week and dont have member or other relivent role to sign up
async def msg_non_members():
    allUsers = client.get_all_members()
    nonMembers = []
    ignoredRoles = ['member', 'Adelaide CSC exec', 'Industry', 'exec']
    for user in allUsers:
        flag = True
        for item in ignoredRoles:
            if check_for_role(user, item) == True:
                flag = True
            if flag == False:
                if (datetime.now() - (user.joined_at.replace(tzinfo=None))).days >= 7:
                    nonMembers.append(user)

    for user in nonMembers:
        if isinstance(user, Member):
            try:
                channel = await user.create_dm()
                await channel.send('Hi,\nyou have been in the UniSA Open Source Community discord for more then a week, and still have not signed up.\nIt only takes a minute to sign up, is free and you dont need to be a UniSA student to do it. Signing up is the best way to support our club and allow us to host as many future events as possible.\nhttps://usasa.sa.edu.au/clubs/join/7520/')
            except discord.errors.HTTPException:
                print(f'{user.name} could not be messaged')

    return f'{[x.name for x in nonMembers]} have all been direct messaged.'


async def test():
    pass


# finds the appropraite function to call based on the message content
async def get_response(message: Message):
    message_content = message.content
    if message_content[0] != '!':
        return False

    if message_content.startswith('!member'):
        return await add_role(message)
    elif message_content.startswith('!spam'):
        return await renew()
    elif message_content.startswith('!msgnonmembers'):
        return await msg_non_members()
    elif message_content.startswith('!test'):
        return await test()


# deals with recived messages
async def send_message(message: Message) -> None:
    message_content = message.content

    if not message_content:
        print('user message is empty')
        return

    response: str = await get_response(message)
    if response != False:
        await message.channel.send(response)


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
