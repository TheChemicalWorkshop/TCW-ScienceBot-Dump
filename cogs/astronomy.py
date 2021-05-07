import discord
from discord.ext import commands
import asyncio

from PIL import Image
import glob, os

import aiohttp

from datetime import timedelta


async def grab_apod(api_key, date_lookup, hd=True):
    async with aiohttp.ClientSession() as session:
        params = {'api_key': api_key,\
            'hd': str(hd), 'date': str(date_lookup.strftime("%Y-%m-%d"))}
        response = await session.get('https://api.nasa.gov/planetary/apod', params=params)
        if (await response.json()).get("url") == None: # no pic found
            current_date_obj = date_lookup - timedelta(days=1)
            return grab_apod(api_key, current_date_obj, hd)
        else:
            return await response.json()




class astronomy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded astronomy")


    @commands.command()
    async def apod(self, ctx):
        from datetime import date, datetime

        current_date_obj = date.today()
        resp = await grab_apod("REMOVED_FOR_PRIVACY", current_date_obj)
        link = ""
        try:
            if resp.get('hdurl'):
                link = resp.get('hdurl')
            elif resp.get('url'):
                link = resp.get('url')
            else:
                link = ""

            await ctx.send(\
                f"Astronomy Picture of the Day ({resp.get('date')})\n"\
                f"by **{resp.get('copyright')}**\n"\
                f"\n"\
                f"{resp.get('explanation')}\n"\
                f"{link}"\
            )
        except:
            await ctx.send("Something went wrong, try again later")
            print(resp)


def setup(bot):
    bot.add_cog(astronomy(bot))
