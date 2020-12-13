from helpers.selections import makeSelections
import time
import discord

from discord import message
from discord import client
from datetime import datetime

client = discord.Client
shouldAutoSave = True


def isCommand(message: discord.Message):
    user = message.author
    if message.content[0] == "!":
        return True
    else:
        return False


async def runCommand(message: discord.Message):
    user = message.author
    command = message.content[1::].split()[0].lower()
    switch = {
        "help": help,
        "userdata": userData,
        "resetuser": resetUser,
        "ops": ops,
        "save": save,
        "load": load,
        "autosave": autoSave,
        "stopautosave": stopAutoSave,
        "makeselections": makeSelections,
    }
    func = switch.get(command, invalid)
    if func == help:
        await help(message)
    elif user not in client.ops:
        await user.send("You do not have permission to do that.")
    else:
        await func(message)


async def invalid(message: discord.Message):
    user = message.author
    await user.send("That is not a valid command.")


async def help(message: discord.Message):
    user = message.author
    async with message.channel.typing():
        time.sleep(5)
        await user.send("Ha, you thought.")


async def userData(message: discord.Message):
    user = message.author
    ret = ""
    async with message.channel.typing():
        for user, info in client.enrolled.items():
            ret += str(user) + "\t*" + str(user.id) + "*\n\t\t`"
            ret += str(info) + "\n`"
    try:
        await user.send(ret)
    except:
        await user.send("Something went wrong. There are probably no users enrolled.")


async def resetUser(message: discord.Message):
    user = message.author
    r_user = await client.fetch_user(message.content.split()[1])
    if r_user in client.enrolled.keys():
        del client.enrolled[r_user]
        await user.send("Removed " + str(user) + " from enrolled.")
    elif r_user in client.denied:
        client.denied.remove(r_user)
        await user.send("Removed " + str(user) + " from denied.")
    else:
        await user.send(str(r_user) + " was not in either list.")
    await client.save()


async def ops(message: discord.Message):
    user = message.author
    ret = ""
    async with message.channel.typing():
        for user in client.ops:
            ret += str(user) + "\t*" + str(user.id) + "*"
    try:
        await user.send(ret)
    except:
        await user.send("Something went wrong.")


async def save(message: discord.Message):
    user = message.author
    try:
        await client.save()
    except Exception as e:
        await user.send("Something went wrong.")
        await user.send(str(e))
        return
    await user.send("Save was successful.")


# This function is broken
async def autoSave(message: discord.Message):
    user = message.author

    # ****
    await user.send("Auto-save is currently broken, use normal save.")
    return
    # ****

    try:
        await client.save()
    except Exception as e:
        await user.send("Something went wrong with auto-save.")
        await user.send(str(e))
        print("Auto-save fail attempt at", datetime.now())
        return
    await user.send("Auto-save was successful. At: `" + str(datetime.now()) + "`")
    for i in range(18000):
        if shouldAutoSave:
            time.sleep(1)
        else:
            return
    return await autoSave(message)


async def stopAutoSave(message: discord.Message):
    user = message.author
    shouldAutoSave = False
    await user.send("Stopping auto-save.")


async def load(message: discord.Message):
    user = message.author
    try:
        await client.load()
    except Exception as e:
        await user.send("Something went wrong.")
        await user.send(str(e))
        return
    await user.send("Load was successful.")
