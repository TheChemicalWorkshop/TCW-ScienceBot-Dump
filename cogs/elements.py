import discord
from discord.ext import commands
import asyncio
from mendeleev import element

class elements(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded elements")

    # @commands.command()
    # async def element(self, ctx, arg):
    #     ele = element(arg)
    #     await ctx.send(ele.density)

    @commands.command()
    async def isotope(self, ctx, arg_unfiltered):
        arg = discord.utils.escape_mentions(arg_unfiltered.lower().title())
        try:
            ele = element(arg)
        except:
            await ctx.send(f"ERROR: {arg} not found !")
            return

        final_msg = ""

        for iso in ele.isotopes:
            if iso.is_radioactive == True:
                radioactive=" ☢"
            else:
                radioactive=""

            if iso.abundance == None:
                abundance = ""
            else:
                abundance = f" ({round(iso.abundance*100, 3)}%)"

            final_msg = f"{final_msg}{ele.name}-{iso.mass_number}{radioactive}{abundance}\n"



        

        await ctx.send(final_msg)



    # @commands.command()
    # async def element(self, ctx, arg_unfiltered):
    #     arg = discord.utils.escape_mentions(arg_unfiltered.lower().title())
    #     try:
    #         ele = element(arg)
    #     except:
    #         await ctx.send(f"ERROR: {arg} not found !")
    #         return

    #     await ctx.send(element)












        # adundance_crust
        # adundance_sea
        # atomic_number
        # atomic_radius
        # atomic_weight
        # block
        # boiling_point
        # cas
        # cpk_color
        # density
        # description
        # discoveries
        # discovery_location
        # discovery_year
        # econf
        # electron_affinity
        # electrons
        # group_id
        # heat_of_formation
        # is_radioactive
        # mass
        # melting_point
        # name
        # name_origin
        # neutrons
        # period
        # protons
        # series
        # sources
        # symbol
        # thermal_conductivity
        # uses
        # 
        # isotopes
        #   abundance
        #   atomic_factor
        #   g_factor
        #   half_life
        #   half_life_unit
        #   id
        #   is_radioactive
        #   mass
        #   mass_number
        #   quadruple_moment
        #   spin



        

def setup(bot):
    bot.add_cog(elements(bot))
