import asyncio
import discord

from discord import message


async def solicitEnroll(user: discord.User, client: discord.Client):
    d_message = await user.send(
        "Hey, are you interested?\nReact with a Christmas tree below if you are.\nIf not, just ignore this message."
    )
    await d_message.add_reaction("🎄")

    def check(reaction, r_user):
        return user == r_user and str(reaction.emoji) == "🎄"

    try:
        await client.wait_for("reaction_add", timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await user.send("You didn't answer.\nThat's okay; I won't ask again.")
        return False
    else:
        await user.send("Sweet! I have a few questions:")
        return True


async def infoGather(user: discord.User, client: discord.Client):
    await user.send(
        "In three (space separated) words, describe your interests.\nThis is just incase your match needs a bit of help selecting something for you."
    )
    info = {}

    def checkInterests(message):
        if user == message.author:
            interests = message.content.split()
            info["interests"] = interests
            return len(interests) == 3
        return False

    await client.wait_for("message", check=checkInterests)
    print(str(user), "has the interests:", info["interests"])

    await user.send("Nice.")
    await user.send(
        "Next question: Have you been naughty or nice this year? (naughty or nice)"
    )

    def checkWasBad(message):
        if user == message.author:
            answer = message.content.lower()
            info["was_bad"] = answer == "naughty"
            return answer in ["naughty", "nice"]
        return False

    await client.wait_for("message", check=checkWasBad)
    print(str(user), "was bad:", info["was_bad"])

    await user.send("Damn straight." if info["was_bad"] else "Cap.")
    await user.send(
        "As a reminder, the budget for this swap has been set at $"
        + str(client.budget)
        + ".\nThat's all. I'll let you know who you get (here, in DM) when selections are made!"
    )
    return info
