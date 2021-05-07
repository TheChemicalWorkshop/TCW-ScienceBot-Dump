import discord
from discord.ext import commands
import asyncio

from datetime import date, datetime, timedelta
import aiohttp

api_key = "REMOVED_FOR_PRIVACY"
RAPI_Host = "wft-geo-db.p.rapidapi.com"



async def lookup_city_data(params):
    async with aiohttp.ClientSession() as session:
        headers={
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
        "X-RapidAPI-Key": "REMOVED_FOR_PRIVACY"
        }
        
        response = await session.get('https://wft-geo-db.p.rapidapi.com/v1/geo/cities?', headers=headers, params=params)

        return await response.json()


async def lookup_city_info(id):
    async with aiohttp.ClientSession() as session:
        headers={
        "X-RapidAPI-Host": RAPI_Host,
        "X-RapidAPI-Key": api_key
        }
        
        response = await session.get(f'https://wft-geo-db.p.rapidapi.com/v1/geo/cities/{id}', headers=headers)

        return await response.json()




class demographics(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded demographics")


    @commands.command()
    async def findcity(self, ctx, city):
        # current_date_obj = date.today()
        params = {\
            'namePrefix': city,\
            'offset': "0",\
            'limit': 5}
        resp = await lookup_city_data(params)
        # print(resp)
        if resp.get("data") == []:
            await ctx.send("result not found :(")
            return
        for city in resp.get("data"):
            await ctx.send(\
                f"id - {city.get('id')}\n"\
                f"country - {city.get('country')}\n"\
                f"name - {city.get('name')}\n"\
                f"region - {city.get('region')}\n"\
            )

    @commands.command()
    async def cityinfo(self, ctx, id):
        # current_date_obj = date.today()
        resp = await lookup_city_info(id)
        # print(resp)

        await ctx.send(\
            f"id - {resp.get('data').get('id')}\n"\
            f"country - {resp.get('data').get('country')}\n"\
            f"name - {resp.get('data').get('name')}\n"\
            f"region - {resp.get('data').get('region')}\n"\
            f"population - {resp.get('data').get('population')}\n"\
            f"timezone - {(resp.get('data').get('timezone')).replace('__', '/')}\n"\
            )
    


def setup(bot):
    bot.add_cog(demographics(bot))
