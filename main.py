import discord
import datetime
from discord.ext.commands import MissingPermissions, has_permissions

from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
ANNOUNCEMENTS = 895310090599559188 # How it works
ROUND_TABLE = 895309794561368064
GENERAL = 895296887408701471
RATS = 895310870148706344

# wrapper for discord.py user class to better serve our purposes
# the global user list (allUsers) should be passed as the userList arguement
class User:
    def __init__(self,id:int,client:discord.Client,userList:dict):
        #adds the new user to the global user list
        userList[id] = self
        self.id = id
        self.userObject:discord.User = client.get_user(id)
        self.userList:dict = userList
        self.name = ""
        self.allegiance:User = None
        self.secretAllegiance:User = None
        self.bannedDate:datetime.datetime = None
        self.permaBanned:bool = False

        self.updateDatabase(True)

    def __str__(self):
        return self.userObject.display_name

    def updateDatabase(self,newEntry:bool = False):
        if newEntry:
            pass
        else:
            pass

    def addRole(self,role):
        pass
    
    def removeRole(self,role):
        pass

    # both of these can accept an id or User instance
    def setAllegiance(self,target):
        if isinstance(target,int):
            target = self.userList[target]
        if not isinstance(target,User):
            print("user not found or invalid type passed to setAllegiance")
            return
        self.allegiance = target
        self.updateDatabase()
    
    def setSecretAllegiance(self,target):
        if isinstance(target,int):
            target = self.userList[target]
        if not isinstance(target,User):
            print("user not found or invalid type passed to setSecretAllegiance")
            return
        self.secretAllegiance = target
        self.updateDatabase()

    def ban(self):
        self.bannedDate = datetime.datetime.now()
        #this probably won't work I just Guessed
        self.userObject.guild.ban(self.userObject)

    def permaBan(self):
        self.permaBanned = True
        self.ban()

    async def message(self,message):
        await self.userObject.dm_channel.send(message)

# government superclass
class Government:
    def __init__(self,leaders):
        self.leaders = leaders
        self.openVotes = []

    # participants are the people who can vote, channel is where the vote takes place, action is function to run if the vote passes, duration is how long the vote will last
    # Example: currentGovernment.startVote(currentGovernment.leaders,ROUND_TABLE,Joeuser.ban())
    def startVote(self,participants,channel,action, duration):
        pass

class Anarchy(Government):
    pass

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
class Motion:
    def __init__(self,initiator,action):
        self.initiator = initiator
        self.supporters = []
        self.action = action

    def support(self,supporter):
        if supporter in self.supporters:
            return "You already support this Cause"
        else:
            self.supporters.append(supporter)
            return "You have pledged your support to this cause"
    
    def passMotion(self):
        self.action()

# also a superclass, this type of motion seeks to start a new government
class TakeOver(Motion):
    def __init__(self,newGovernment:Government):
        super().__init__(self)
        self.newGovernment = newGovernment

    def passMotion(self):
        global currentGovernment
        currentGovernment = self.newGovernment

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
