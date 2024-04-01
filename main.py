import discord

from config import TOKEN


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        if message.content.startswith("ban"):
            user = message.content.split()[1]
            print(f"Ban user: {user}")
            # ban function


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
