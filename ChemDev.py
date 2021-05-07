import discord
from discord.ext import commands, tasks
from itertools import cycle
import os

import aiohttp
import asyncio
import async_timeout
import ssl
import json

import random

from extra_commands import prefix_management, beta_optin_management

bot = commands.Bot(command_prefix=prefix_management.get_prefix, intents=discord.Intents.all())

devs = [446959856318939137, 589968097369128966] # ! my bot 589968097369128966
bot.remove_command('help')

bot.blacklists = []
bot.donators = []

# SPACER --------------------------------------- SPACER
# SPACER --------------------------------------- SPACER
# SPACER --------------------------------------- SPACER

# ! general fetch
async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

# ! grabs blacklists
async def get_blacklists():
    async with aiohttp.ClientSession(headers={"token": "REMOVED_FOR_PRIVACY"}) as session:
        web_content = json.loads(await fetch(session, 'http://api.thechemicalworkshop.com/api/blacklists'))
        return web_content

# ! grabs donators, money = paid
async def get_donators(money=False): # if True, shows only paid
    async with aiohttp.ClientSession(headers={"token": "REMOVED_FOR_PRIVACY"}) as session:
        web_content = json.loads(await fetch(session, 'http://api.thechemicalworkshop.com/api/donators'))
        
        def check_money_and_active(value):
            if value.get("money") == True and value.get("active") == True:
                return True
            else:
                return False

        def check_active(value):
            if value.get("active") == True:
                return True
            else:
                return False
        
        if money == False:
            return list(filter(check_active, web_content))
        else:
            return list(filter(check_money_and_active, web_content))

def verify_donator(discord_id):
    for user in bot.donators:
        if user.get("discord_id") == discord_id and user.get("active"):
            return True
    return False

def verify_blacklist(discord_id):
    for user in bot.blacklists:
        if user.get("discord_id") == discord_id and user.get("active"):
            return True
    return False


def dev_check(ctx):
    return str(ctx.author.id) in str(devs)

def grab_thanks():

    this_bot_thanks = [\
    "Special thanks to Noah205 for making this bot possible !",
    "Join TCW ! | Discord.TheChemicalWorkshop.com",
    "Special thanks to ReactiveChem Community for beta testing ! | reactivechem.tk",
    "TCW offers more bots ! | Discord.TheChemicalWorkshop.com",
    "Join TCW for support ! | Discord.TheChemicalWorkshop.com",
    "Bots don't run themselves, consider donating ! | Discord.TheChemicalWorkshop.com"]

    # if random.randint(0,100) < 35: # donators PAID
    #     return f"Special thanks to {bot.donators_money[random.randint(0,len(bot.donators_money)-1)].get('name')} for making this bot possible !"
    # else:
    return this_bot_thanks[random.randint(0,len(this_bot_thanks)-1)]



@bot.command()
@commands.check(dev_check)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Loaded !")


@bot.command()
@commands.check(dev_check)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Unloaded !")


@bot.command()
@commands.check(dev_check)
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Reloaded !")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# ! every 10 mins cache blacklists
@tasks.loop(seconds=600) # every 10 minuts
async def grab_blacklists():
    bot.blacklists = await get_blacklists()

# ! every 10 mins cache donators (paid and not paid)
@tasks.loop(seconds=600) # every 10 minuts
async def grab_donators():
    bot.donators = await get_donators()
    bot.donators_money = await get_donators(True)


@bot.event
async def on_connect():
    # ! verify user
    bot.verify = verify_donator
    bot.black = verify_blacklist

    bot.check_beta = beta_optin_management.get_beta_optin

    # ! enable and start cache
    bot.blacklists = await get_blacklists()
    grab_blacklists.start()
    bot.donators = await get_donators()
    bot.donators_money = await get_donators(money=True)
    grab_donators.start()
    
    # ! asign thanks to bot.thanks
    bot.thanks = grab_thanks



@bot.event
async def on_ready():
    print("ChemDev Bitches")
    # TODO change activity to smth... a loop, not sure what
    await bot.change_presence(activity=discord.Game(name="THIS IS BETA !"))


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------


bot.run("REMOVED_FOR_PRIVACY")
# ! TESTSERVER OPEN


