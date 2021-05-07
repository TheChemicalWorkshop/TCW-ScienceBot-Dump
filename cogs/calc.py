import discord
from discord.ext import commands
import asyncio
from chempy import balance_stoichiometry, mass_fractions


class calc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded calc")


    @commands.command()
    async def balance(self, ctx, *, cmp_unfiltered):
        cmp = discord.utils.escape_mentions(cmp_unfiltered)
        cmp = cmp.replace("+", " ")
        if "->" in cmp:
            splitcmp = cmp.split("->")
        elif ">" in cmp:
            splitcmp = cmp.split(">")
        elif "=" in cmp:
            splitcmp = cmp.split("=")
        else:
            await ctx.send("An equasion has an = sign !")
            return
        reactant = splitcmp[0].split(" ")
        reactant[:] = [x for x in reactant if x]
        product = splitcmp[1].split(" ")
        product[:] = [x for x in product if x]

        # print(splitcmp)
        # print(set(reactant))  # ! debug
        # print(set(product))   # ! debug
        # reac, prod = balance_stoichiometry({'H2', 'O2'}, {'H2O'})
        try:
            reac, prod = balance_stoichiometry(set(reactant), set(product))
        except Exception as err:
            await ctx.send(err)
            return

        embed = discord.Embed(
        colour=discord.Colour(0x3b12ef),
        description="Made possible by TCW",
        )

        reaction = []
        for fractions in map(mass_fractions, [reac, prod]):
            reaction.append({k: '{0:.3g} wt%'.format(v*100) for k, v in fractions.items()})
        # print(reaction)


        embed.set_author(
            name=f"Your balanced reaction:",
            url=f"http://www.thechemicalworkshop.com/", 
            icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png" # ! edit
            )
        embed.set_footer(
            text=f"{self.bot.thanks()}",
            icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
            )

        _i = 1
        for i in reaction:
            for reactant, product in i.items():
                print(reactant)
                embed.add_field(name=reactant, value=product, inline=False)

            if _i == 1:
                embed.add_field(name="🠙🠙🠙 Reactants 🠙🠙🠙", value="🠛🠛🠛 Products 🠛🠛🠛", inline=True)
                _i = 2
            
        await ctx.send(content="", embed=embed)




def setup(bot):
    bot.add_cog(calc(bot))
