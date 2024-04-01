import discord
from discord.ext.commands import MissingPermissions, has_permissions

from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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
