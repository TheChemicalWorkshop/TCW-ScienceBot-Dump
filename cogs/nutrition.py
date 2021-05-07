import discord
from discord.ext import commands
import asyncio

from datetime import date, datetime, timedelta
import aiohttp

api_key = "REMOVED_FOR_PRIVACY"
api_id = "REMOVED_FOR_PRIVACY"
api_user_id = "1"

# left_emoji = "<a:left:833744177249779732>" #testserver
# right_emoji = "<a:right:833744176913973249>" #testserver

left_emoji = "<a:left_arrow:833744993607745586>" #TCW
right_emoji = "<a:right_arrow:833744993457405972>" #TCW

id_to_nutrients = {
  301: ["Calcium", "mg"],
  208: ["Energy", "kcal"],
  303: ["Iron", "mg"],
  306: ["Potassium", "mg"],
  307: ["Sodium", "mg"],
  203: ["Proteins", "g"],
  262: ["Caffeine", "mg"],
  312: ["Copper", "mg"],
  313: ["Fluoride", "µg"],
  212: ["Fructose", "g"],
  287: ["Galactose", "g"],
  211: ["Glucose (Dextrose)", "g"],
  210: ["Sucrose", "g"],
  304: ["Magnesium", "mg"],
  415: ["VItamin B6", "mg"],
  606: ["Total Fatty acids", "g"],
  204: ["Total lipid (fat)", "g"],
  205: ["Carbohydrate, by difference", "g"],
  430: ["Vitamin K (Phylloquinone)", "mg"]
    }



async def lookup_food(food_name):
    async with aiohttp.ClientSession() as session:
        headers={
        "x-app-key": api_key,
        "x-app-id": api_id,
        "x-remote-user-id": api_user_id
        }
        
        response = await session.get(f'https://trackapi.nutritionix.com/v2/search/instant?query={food_name}', headers=headers)

        return await response.json()

async def lookup_food_details(food_name):
    async with aiohttp.ClientSession() as session:
        headers={
            "x-app-key": api_key,
            "x-app-id": api_id,
            "x-remote-user-id": api_user_id
            }
        data={\
            "query": food_name
            }
        response = await session.post(f'https://trackapi.nutritionix.com/v2/natural/nutrients', headers=headers, data=data)

        return await response.json()





class nutrition(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded nutrition")


    def createdetailedfoodembed(self, ctx, detailed_food_reponse, cur_page):
        embed = discord.Embed(
            title=f"{detailed_food_reponse.get('foods')[cur_page-1].get('food_name')}",
            colour=discord.Colour(0x3b12ef),
            # url="https://discordapp.com/",
            description=\
                f"served as: {detailed_food_reponse.get('foods')[cur_page-1].get('serving_unit')}\n"\
                f"= {detailed_food_reponse.get('foods')[cur_page-1].get('serving_weight_grams')} g\n"
            )
        # {help_obj[cur_page-1].get('image_url')}
        # if food.get('photo').get("highres"):
        #     await ctx.send(food.get('photo').get("highres"))
        if detailed_food_reponse.get("foods")[cur_page-1].get('photo').get("highres"):
            embed.set_image(url=detailed_food_reponse.get("foods")[cur_page-1].get('photo').get("highres"))
        # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/1.png")
        embed.set_author(
            name=ctx.bot.user.display_name,
            icon_url=ctx.bot.user.avatar_url
            )
        embed.set_footer(
            text=f"{self.bot.thanks()}",
            icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
            )

        for nutrient in detailed_food_reponse.get('foods')[cur_page-1].get('full_nutrients'):
                if nutrient.get("attr_id") in id_to_nutrients and nutrient.get("value") != 0:
                    ntr = id_to_nutrients.get(nutrient.get('attr_id'))
                    embed.add_field(
                        name=f"{ntr[0]}:",
                        value=f"{nutrient.get('value')} {ntr[1]}",
                        inline=True
                        )
                    # food_str += f"{ntr[0]}: {nutrient.get('value')} {ntr[1]}\n"

        return embed


    @commands.command()
    async def foodinfo(self, ctx, *, foodname):


        #! FIX DONATORS
        premium = False    

        for donator in self.bot.donators:
            if \
                ctx.author.id == donator.get("discord_id") or \
                ctx.guild.owner_id == donator.get("discord_id") or\
                ctx.guild.id == 450914543619538955 or\
                ctx.guild.id == 644966555930853390:
                    premium = True
        #! FIX DONATORS

        print(len(foodname))
        if len(foodname) > 220 and premium == False:
            await ctx.send(\
                f"hey {ctx.author.name} you entered {len(foodname)} characters\n"\
                f"If you REALLY wanna list this much food upgrade to premium\n"
                f"or don't and reduce your search to 200 or less characters")
            return

        # current_date_obj = date.today()
        params = {}
        # resp = await lookup_food(foodname)
        # print(resp)
        resp = await lookup_food_details(foodname)
        # print(resp)
        if not resp.get("foods"):
            await ctx.send("We couldn't match any of your foods")
            return



        #* starter variables
        timeout_time = 60 # 1 min
        pages = len(resp.get("foods"))
        cur_page = 1

        #* embed with edit
        embed = self.createdetailedfoodembed(ctx, resp, cur_page)
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
                    embed = self.createdetailedfoodembed(ctx, resp, cur_page)
                    await message.edit(
                        content=f"`Page {cur_page}/{pages}:`\n\n",
                        embed=embed)
                    #* embed with edit

                    await message.remove_reaction(reaction, user)

                #* PREVIOUS PAGE
                elif str(reaction.emoji) == left_emoji and cur_page > 1:
                    cur_page -= 1


                    #* embed with edit
                    embed = self.createdetailedfoodembed(ctx, resp, cur_page)
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

    @commands.command()
    async def food2(self, ctx, *, foodname):
        # current_date_obj = date.today()
        params = {}
        resp = await lookup_food(foodname)
        # print(resp)
        if not resp.get("common") and not resp.get("branded"):
            await ctx.send("We couldn't match any of your foods")
            return

        common_list = "---Common food ---\n\n"
        i = 0
        for com in resp.get("common"):
            common_list += f"food name = {com.get('food_name')}\n"
            common_list += f"serving unit = {com.get('serving_unit')}\n"
            common_list += f"serving qty = {com.get('serving_qty')}\n\n"
            i+=1
            if i == 5:
                break
        await ctx.send(common_list)

        branded_list = "---branded food ---\n\n"
        i = 0
        for com in resp.get("branded"):
            branded_list += f"offical name = {com.get('brand_name_item_name')}\n"
            branded_list += f"food name = {com.get('food_name')}\n"
            branded_list += f"serving unit = {com.get('serving_unit')}\n"
            branded_list += f"serving qty = {com.get('serving_qty')}\n"
            branded_list += f"brand name = {com.get('brand_name')}\n\n"
            i+=1
            if i == 5:
                break
        await ctx.send(branded_list)



def setup(bot):
    bot.add_cog(nutrition(bot))
