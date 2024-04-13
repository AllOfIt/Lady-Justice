import datetime

import discord
from discord.ext.commands import MissingPermissions, has_permissions

from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
ANNOUNCEMENTS = 895310090599559188  # How it works
ROUND_TABLE = 895309794561368064
GENERAL = 895296887408701471
RATS = 895310870148706344


# superclass for anything you can lend your support to
class Supportable:
    def __init_subclass__(self):
        self.name = ""
        self.supporters = []
        self.secret = False

    def __str__(self):
        return self.name

    # supporter should be a User instance but ":User" causes an error because its not difined yet :(
    def support(self, supporter):
        if supporter in self.supporters:
            return f"You already support {self}"
        self.supporters.append(supporter)
        return f"You have pledged your support to {self}"

    # same issue with ":User"
    def removeSupport(self, supporter):
        if supporter in self.supporters:
            self.supporters.remove(supporter)
            return f"You have withdrawn your support from {self}"
        return f"You don't support {self}]"


# wrapper for discord.py user class to better serve our purposes
# the global user list (allUsers) should be passed as the userList arguement
class User(Supportable):
    def __init__(self, id: int, client: discord.Client, userList: dict):
        # adds the new user to the global user list
        userList[id] = self
        self.id = id
        self.userObject: discord.User = client.get_user(id)
        self.userList: dict = userList
        self.name = ""
        self.allegiance: User = None
        self.secretAllegiance: User = None
        self.bannedDate: datetime.datetime = None
        self.permaBanned: bool = False
        self.supporters = []

        self.updateDatabase(True)

    def __str__(self):
        return self.userObject.display_name()

    def updateDatabase(self, newEntry: bool = False):
        if newEntry:
            pass
        else:
            pass

    def addRole(self, role):
        pass

    def removeRole(self, role):
        pass

    # todo: this needs fixing
    # target for both of these can be any supportable
    def setAllegiance(self, target):

        self.allegiance = target

        self.updateDatabase()

    def setSecretAllegiance(self, target):
        pass

    def ban(self):
        self.bannedDate = datetime.datetime.now()
        # this probably won't work I just Guessed
        self.userObject.guild.ban(self.userObject)

    def permaBan(self):
        self.permaBanned = True
        self.ban()

    async def message(self, message):
        await self.userObject.dm_channel.send(message)


# government superclass
class Government(Supportable):
    def __init__(self, leaders):
        self.leaders = leaders
        self.openVotes = []
        self.openMotions = []

    # participants are the people who can vote, channel is where the vote takes place, action is function to run if the vote passes, duration is how long the vote will last
    # Example: currentGovernment.startVote(currentGovernment.leaders,ROUND_TABLE,Joeuser.ban())
    def startVote(self, participants, channel, action, duration):
        pass


class Anarchy(Government):
    def __init__(self):
        Government.__init__(self,[])



class Dictatorship(Government):
    pass


class Monarchy(Government):
    pass


class Oligarchy(Government):
    pass


class Democracy(Government):
    pass


class Republic(Government):
    pass


# Motion Superclass that lets player define a power move and set their allegiance to it before it takes effect
class Motion(Supportable):
    def __init__(self, name: str, initiator: User, government: Government, action = ...,**kwargs):
        self.name = name
        self.initiator = initiator
        self.government = government
        self.supporters = []
        self.action = action
        self.government.openMotions.append(self)
        if "message" in kwargs:
            self.successMessage = kwargs["message"]
        else:
            self.successMessage = "Motion passed"
        self.failMessage = "Motion Failed"

    def delete(self):
        for supporter in self.supporters:
            if supporter.allegiance == self:
                supporter.allegiance = None
            if supporter.secretAllegiance == self:
                supporter.secretAllegiance = None
        self.government.openMotions.remove(self)

    def passMotion(self):
        self.action()
        self.delete()
        return self.successMessage
    
    def failMotion(self):
        self.delete()
        return self.failMessage



# also a superclass, this type of motion seeks to start a new government
class TakeOver(Motion):
    def __init__(self,name:str,initiator:User, currentGovernment:Government,action, newGovernment: Government):
        Motion.__init__(self,name,initiator,currentGovernment,action)
        self.newGovernment = newGovernment

    def passMotion(self):
        self.delete()
        global currentGovernment
        currentGovernment = self.newGovernment


class Coup(TakeOver):
    pass

class Revolt(TakeOver):
    pass

# a secret motion to kill
class Assassination(Motion):
    def __init__(self,target):
        self.secret = True
        ...

class Vote:
    def __init__(self):
        pass


allUsers = {}
currentGovernment = Anarchy()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("ban"):
        user_id = message.content.split()[1]

        # todo right now this only prints out the bot's member information
        # why can't it see the other members?
        print(message.guild.members)
        print(f"ban: {user_id}")


@client.event
async def ban(
    user, *, reason=None, delete_message_days=..., delete_message_seconds=...
):
    print(f"Banning {user}")


client.run(TOKEN)
