#! /usr/bin/python3
from tokens import *
from settings import *
from game import *
from discord import Game
import discord
import sys

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith(BOT_PREFIX + "help"):
        msg = ("!help - prints this help\n"
               "!ping - simple online check\n"
               "!start GAME - starts a server for GAME\n"
               "!stop GAME - stops the server for GAME\n"
               "!status [GAME] - prints basic infos about the server for GAME\n"
               "!exit - exit bot script - should restart it when used with systemd service unit"
               ).format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith(BOT_PREFIX + "ping"):
        msg = "I'm online {0.author.mention}".format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith(BOT_PREFIX + "start"):
        cmd = message.content.split("start", 1)[1].lower().split()
        if not cmd:
            msg = ("Syntax error:\n"
                   "!start GAME"
                   )
        else:
            for i in GAMES:
                if i.name.lower() == cmd[0]:
                    if i.isRunning() == False:
                        await client.change_presence(game=Game(name="starting server..."))
                        await i.start()
                        await client.change_presence(game=Game(name="ready"))
                    msg = i.status()
        await client.send_message(message.channel, msg)
    elif message.content.startswith(BOT_PREFIX + "stop"):
        cmd = message.content.split("stop", 1)[1].lower().split()
        if not cmd:
            msg = ("Syntax error:\n"
                   "!stop GAME"
                   )
        else:
            for i in GAMES:
                if i.name.lower() == cmd[0]:
                    if i.isRunning() == True:
                        await client.change_presence(game=Game(name="stopping server..."))
                        await i.stop()
                        await client.change_presence(game=Game(name="ready"))
                    msg = i.status()
        await client.send_message(message.channel, msg)
    elif message.content.startswith(BOT_PREFIX + "status"):
        cmd = message.content.split("status", 1)[1].lower().split()
        for i in GAMES:
            if not cmd:
                msg = i.status()
            elif i.name.lower() == cmd[0]:
                msg = i.status()
            await client.send_message(message.channel, msg)
    elif message.content.startswith(BOT_PREFIX + "exit"):
        sys.exit("exit requested")

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    await client.change_presence(game=Game(name="ready"))

client.run(DISCORD_TOKEN)
