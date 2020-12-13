import asyncio
import discord
import random
import json

client = discord.Client

# Archetype for entries in the enrolled dictionary
Enrolled = {discord.User: {str: [str, str, str], str: bool}}


def parseEnrolled(enrolled: Enrolled):
    matches = {}
    users = list(enrolled.keys())
    random.shuffle(users)
    for i in reversed(range(len(users))):
        matches[users[i]] = users[i - 1]
    return matches


async def makeSelections(message: discord.Message):
    user = message.author
    await user.send("Making selections...")
    matches = parseEnrolled(client.enrolled)
    saveData = []
    for (giver, recip) in matches.items():
        saveData.append((giver.name, recip.name))
        ret = "Congrats, selections have been made!\nThe person you're gifting to is... **"
        ret += recip.name + "**\n"
        ret += (
            "Their interests include:\t`"
            + str(client.enrolled[recip]["interests"])
            + "`"
        )
        d_message = await giver.send(ret)
        await d_message.add_reaction("🧑‍🎄")
        await d_message.add_reaction("✨")
        await d_message.add_reaction("🎁")

        d_message = await giver.send(
            "Remember, the maximum allowed budget for a gift is $"
            + str(client.budget)
            + ". Merry Chrysler!"
        )
        await d_message.add_reaction("🤑")

    try:
        with open("matches.json", "w") as outfile:
            json.dump(json.dumps(saveData), outfile, indent=4)
    except Exception as e:
        await user.send("Something went wrong.")
        await user.send(str(e))
        return
    await user.send("Matches save was successful.")

    # End the program
    exit