import discord
import datetime
from discord.ext.commands import MissingPermissions, has_permissions

from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# wrapper for discord.py user class to better serve our purposes
class User:
    def __init__(self,id:int,client:discord.Client):
        self.userObject:discord.User = client.get_user(id)
        self.name = ""
        self.allegiance:User = None
        self.secretAllegiance:User = None
        self.bannedDate:datetime.datetime = None
        self.permaBanned:bool = False

        self.updateDatabase(True)

    def updateDatabase(self,newEntry:bool = False):
        if newEntry:
            pass
        else:
            pass

    def addRole(self,role):
        pass
    
    def removeRole(self,role):
        pass

    #might need a system for searching for the right user class, maybe a dict
    def setAllegiance(self,target):
        self.allegiance = target
        self.updateDatabase()
    
    def setSecretAllegiance(self,target):
        self.secretAllegiance = target
        self.updateDatabase()

    def ban(self):
        self.bannedDate = datetime.datetime.now()
        #this probably won't work I just Guessed
        self.userObject.guild.ban(self.userObject)

    def permaBan(self):
        self.bannedDate = None
        self.permaBanned = True
        self.userObject.guild.ban(self.userObject)

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
