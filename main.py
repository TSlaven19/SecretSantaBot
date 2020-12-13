import discord
import json
import os

from helpers import interactions
from helpers import commands
from helpers import selections
from discord.enums import ChannelType


class SecretSanta(discord.Client):
    budget = os.environ.get("BUDGET") or 0
    enrolled = {}
    denied = set()
    ops = set()

    async def save(self):
        enrolled_id = {k.id: v for k, v in self.enrolled.items()}
        denied_id = [u.id for u in self.denied]
        ops_id = [u.id for u in self.ops]
        data = []
        data.append(json.dumps(enrolled_id))
        data.append(json.dumps(denied_id))
        data.append(json.dumps(ops_id))
        with open("data.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

    async def load(self):
        data = []
        with open("data.json") as infile:
            data = json.load(infile)
        self.enrolled = {
            (await client.fetch_user(k)): v
            for k, v in eval(
                data[0].replace("false", "False").replace("true", "True")
            ).items()
        }
        self.denied = {(await client.fetch_user(id)) for id in eval(data[1])}
        self.ops = {(await client.fetch_user(id)) for id in eval(data[2])}
        print("Data loaded:")
        print("\tEnrolled:\t", self.enrolled)
        print("\tDenied:\t\t", self.denied)
        print("\tOps:\t\t", self.ops)

    async def on_connect(self):
        try:
            await self.load()
        except Exception as e:
            print(e)
            print(
                "Error loading save data; file probably doesn't exist yet. Will create now."
            )
            await self.save()

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))
        if len(self.ops) < 1:
            self.ops.add(await client.fetch_user(os.environ.get("OPID")))

        game = discord.Game("with elf butthole")
        await client.change_presence(status=discord.Status.online, activity=game)

    async def on_message(self, message):
        user = message.author

        if user.bot:
            return

        if message.channel.type == ChannelType.private and commands.isCommand(message):
            print(str(user), "sent command", message.content)
            await commands.runCommand(message)
            return

        # Solicit on message send in one of the text channels - only if the user has not already been contacted
        elif user not in self.enrolled.keys() and user not in self.denied:
            accepted = await interactions.solicitEnroll(user, client)
            if accepted:
                self.enrolled[user] = "TBD... collecting"
                print(str(user), "added to enrolled list.")

                # Run scripted data collection
                info = await interactions.infoGather(user, client)
                self.enrolled[user] = info
            else:
                self.denied.add(user)
                print(str(user), "added to denied list.")

            await self.save()


client = SecretSanta()
commands.client = client
selections.client = client

client.run(os.environ.get("BOTKEY"))
