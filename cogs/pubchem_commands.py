import discord
from discord.ext import commands
import asyncio

import pubchempy as pcp

discord_numbers =	{
    0: "0️⃣",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣"
}

numbers_discord =	{
    "0️⃣": 0,
    "1️⃣": 1,
    "2️⃣": 2,
    "3️⃣": 3,
    "4️⃣": 4,
    "5️⃣": 5,
    "6️⃣": 6,
    "7️⃣": 7,
    "8️⃣": 8,
    "9️⃣": 9
}

async def lookup_compound(cmp_cid):
    c = pcp.Compound.from_cid(cmp_cid)
    return c

def size_check_256(txt):
    if txt is None:
        return "iupac name Not Found"
    # print(len(txt))
    if len(txt) < 255:
        return txt
    else:
        short = (str(txt[:100])+ " .....")
        return short

class pubchem_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded pubchem_commands")
    

    @commands.command()
    async def search(self, ctx, *, cmp_unfiltered):
        cmp = discord.utils.escape_mentions(cmp_unfiltered)
        # print(discord.utils.escape_mentions(cmp))
        message = await ctx.send("searching... " + cmp)
        cidsRes=pcp.get_cids(cmp, 'name', 'substance', list_return='flat')
        if len(cidsRes) >= 25:
            await message.edit(content=f"Sorry, we are not gonna process your {len(cidsRes)} results\nBe more specific with your search !")
            return
        results =[pcp.Compound.from_cid(cid) for cid in cidsRes]
        if len(results) >= 9:
            await message.edit(content=f"Your result is >9 ({len(results)}), trimming...")
            results = results[:9]
        else:
            if len(results) >= 25:
                pass
            await message.edit(content=f"Processing your {len(results)} results...")
        #results = pcp.get_compounds(cmp, 'name')
 
        # ! if there are no results, print text below
        if not results: 
            await message.edit(content=f"0 results for {cmp} 😟")
            return

        # ! makes one big string, if there are too many results say that aswell
        results_str = ""
        results_ammount = 0
        for i in results:
            results_ammount += 1
            name = "Synonym not found"
            if len(i.synonyms) is not 0:
                name = i.synonyms[0]

            results_str = results_str + f"{discord_numbers.get(results_ammount)} {name} \n"
            # print(i)
        # print(results_str)

        if len(results_str) >= 1900:
            await message.edit(content="Can't show the list, it's bigger than 1900 characters !")
            return

        # print(results)
        # await message.edit(content="newcontent")

        # ! edit the message and show results
        await message.edit(content=results_str)

        # message_id = message.id

        # ! add all the reactions from 1++
        i = 1
        while i <= results_ammount:
            await message.add_reaction(discord_numbers.get(i))
            i += 1
        
        # ! checks if same user reacted with an emoji, timeout 50 seconds
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            # ! timeout
            await message.add_reaction("❌")
        else:
            # ! user reacted with an emoji
            # ! if() user reacted with emoji other than numbers
            # ! bunch of easter eggs, code stops/returns if user reacted with 
            # ! smth else than number
            if numbers_discord.get(reaction.emoji) == None:
                easter_egg_yellow = [662369334059991051, 707003234945990667]
                easter_egg_emojis = ["🇫"]
                print(reaction.emoji)
                if reaction.emoji in easter_egg_emojis:
                    await message.add_reaction("💩")
                    return
                elif reaction.emoji.id in easter_egg_yellow:
                    await message.edit(content="YELLOW DETECTED")
                    return
                else:
                    await message.add_reaction("❌")
                    return

            # await ctx.send(numbers_discord.get(reaction.emoji))
            try:
                selected_cmp = results[numbers_discord.get(reaction.emoji) - 1]
            except IndexError:
                await message.edit(content=f"You know this number can't be selected, I know this number can't be selected, so why? {ctx.author.mention}")
                await asyncio.sleep(5)
                await message.edit(content=f"Enjoy YELLOWCHEM {ctx.author.mention} !")
                return

            await message.edit(content="grabbing data...")

            # ! gives 3d shit
            # ! gives 3d shit
            # ! gives 3d shit
            # cmpdataz = pcp.get_compounds('Aspirin', 'name', record_type='3d')
            # await ctx.send(selected_cmp)


            # print(await lookup_compound(results[numbers_discord.get(reaction.emoji) - 1].cid))
            # print("")
            # await ctx.send(reaction.emoji)
            # print(reaction.emoji)
            import datetime

            pass
        
            selected_cmp_name = "Synonym not found"
            if len(selected_cmp.synonyms) is not 0:
                selected_cmp_name = selected_cmp.synonyms[0]

            embed = discord.Embed(
            # title=selected_cmp.synonyms[0],
            colour=discord.Colour(0x3b12ef),
            # url="https://discordapp.com/",
            description=size_check_256(selected_cmp.iupac_name),
            # timestamp=datetime.datetime.utcfromtimestamp(1580842764) # or any other datetime type format.
            )
            # ! embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_thumbnail(url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{selected_cmp.cid}/PNG?record_type=3d&image_size=small")
            embed.set_author(
                name=f"{selected_cmp_name} ({selected_cmp.cid})",
                url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{selected_cmp.cid}", 
                icon_url="https://pubchem.ncbi.nlm.nih.gov/pcfe/logo/PubChem_logo_splash.png"
                )
            embed.set_footer(
                text=f"{self.bot.thanks()}",
                icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
                )

            embed.add_field(
                name="Molecular Formula",
                value=selected_cmp.molecular_formula
                )
            embed.add_field(
                name="Molecular Weight",
                value=selected_cmp.molecular_weight
                )
            embed.add_field(
                name="Charge",
                value=selected_cmp.charge
                )
            # embed.add_field(
            #     name="another field title",
            #     value="try exceeding some of them! (coz idk them)"
            #     )
            # embed.add_field(
            #     name=":thinking: this supports emotes! (and custom ones too)",
            #     value="if you exceed them, the error will tell you which value exceeds it."
            #     )

            # embed.add_field(
            #     name="Inline",
            #     value="these last two fields",
            #     inline=True
            #     )
            # embed.add_field(
            #     name="Fields",
            #     value="are inline fields",
            #     inline=True
            #     )

            await message.edit(content="", embed=embed)
            # await message.channel.send(
            #     # content="This is a normal message to be sent alongside the embed",
            #     embed=embed
            #     )






        

def setup(bot):
    bot.add_cog(pubchem_commands(bot))
