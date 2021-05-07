import discord
from discord.ext import commands
import asyncio
import aiohttp
import os

# left_emoji = "<a:left:833744177249779732>" #testserver
# right_emoji = "<a:right:833744176913973249>" #testserver

left_emoji = "<a:left_arrow:833744993607745586>"
right_emoji = "<a:right_arrow:833744993457405972>"

max_synonims = 5

trefle_api_key = "REMOVED_FOR_PRIVACY"

async def search_plants(keyword="coconut"):
    async with aiohttp.ClientSession() as session:
        params = {'token': trefle_api_key,\
            'q': str(keyword)}
        response = await session.get('https://trefle.io/api/v1/plants/search?', params=params)
     
        return await response.json()




class botany(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded botany")


    def createplantembed(self, ctx, plant_reponse, cur_page):
        embed = discord.Embed(
            title=f"{plant_reponse.get('data')[cur_page-1].get('common_name')}",
            colour=discord.Colour(0x3b12ef),
            # url="https://discordapp.com/",
            description=\
                f"Slug = {plant_reponse.get('data')[cur_page-1].get('slug')}\n"
                f"Scientific name = {plant_reponse.get('data')[cur_page-1].get('scientific_name')}\n"\
                f"Genus = {plant_reponse.get('data')[cur_page-1].get('genus')}\n"\
                f"Family = {plant_reponse.get('data')[cur_page-1].get('family')}\n"
            )
        # {help_obj[cur_page-1].get('image_url')}
        if plant_reponse.get("data")[cur_page-1].get("image_url"):
            embed.set_image(url=plant_reponse.get("data")[cur_page-1].get("image_url"))
        # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/1.png")
        embed.set_author(
            name=ctx.bot.user.display_name,
            icon_url=ctx.bot.user.avatar_url
            )
        embed.set_footer(
            text=f"{self.bot.thanks()}",
            icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
            )
        synonyms_str = ""
        i = 0
        for synonym in plant_reponse.get("data")[cur_page-1].get('synonyms'):
            synonyms_str += f"{synonym}\n"
            i += 1
            if i == max_synonims:
                break

        if synonyms_str != "":
            embed.add_field(
                name="Synonyms",
                value=synonyms_str,
                inline=True
                )

        return embed


    @commands.command(aliases = [])
    async def searchplant(self, ctx, *, pt):
        resp = await search_plants(pt)
        # print(resp)

        # help_obj = resp.get("data")
        
        #* starter variables
        timeout_time = 60 # 1 min
        pages = len(resp.get("data"))
        cur_page = 1

        #* embed with edit
        embed = self.createplantembed(ctx, resp, cur_page)
        message = await ctx.send(
            content=f"`Page {cur_page}/{pages}:`\n\n",
            embed=embed
            )
        #* embed with edit


        await message.add_reaction(left_emoji)
        await message.add_reaction(right_emoji)

        def check(reaction, user):
            if reaction.message.id == message.id:
                return user == ctx.author and str(reaction.emoji) in [left_emoji, right_emoji]
            # This makes sure nobody except the command sender can interact with the "menu"
            # The check on top ensures that the reaction is placed on correct message

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout_time, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                #* NEXT PAGE
                if str(reaction.emoji) == right_emoji and cur_page != pages:
                    cur_page += 1

                    #* embed with edit
                    embed = self.createplantembed(ctx, resp, cur_page)
                    await message.edit(
                        content=f"`Page {cur_page}/{pages}:`\n\n",
                        embed=embed)
                    #* embed with edit

                    await message.remove_reaction(reaction, user)

                #* PREVIOUS PAGE
                elif str(reaction.emoji) == left_emoji and cur_page > 1:
                    cur_page -= 1


                    #* embed with edit
                    embed = self.createplantembed(ctx, resp, cur_page)
                    await message.edit(
                        content=f"`Page {cur_page}/{pages}:`\n\n",
                        embed=embed)
                    #* embed with edit

                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds






def setup(bot):
    bot.add_cog(botany(bot))
