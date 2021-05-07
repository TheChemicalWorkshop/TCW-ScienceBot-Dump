import discord
from discord.ext import commands
import asyncio
from chempy import balance_stoichiometry, mass_fractions

from PIL import Image
import glob, os

import lists.visiblespectrum as visiblespectrum
# from lists.visiblespectrum import visiblespectrum

from PIL import Image
import glob, os
from io import BytesIO 

deepkek = "<:deepkek:736669809110155344>"
infrared = "<:UltraHarold:771104447501172737>"

yellowchem = "<:yellowchem:717858591335514112>"

class physics(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded physics")


    @commands.command()
    async def nm(self, ctx, nm):

        #* nani easter egg
        if nm.lower() == "nani":
            await ctx.send(yellowchem)
            return
        #* nani easter egg

        try:
            wavelenght = float(nm)
        except Exception as err:
            await ctx.send("ERROR")
            return

        if wavelenght < 380:
            msg = await ctx.reply(f"{wavelenght}nm - Looks like cancer (invisible)")
            await asyncio.sleep(10)
            await msg.edit(content = deepkek)
            return
        if wavelenght > 780:
            msg = await ctx.reply(f"{wavelenght}nm - Looks like infrared or higher (invisible)")
            await asyncio.sleep(10)
            await msg.edit(content = infrared)
            return

        img = Image.new('RGB', (1024, 1024), color = visiblespectrum._wavelength_to_rgb(wavelenght))
        # img.save('pil_color.png')
        print(visiblespectrum._wavelength_to_rgb(wavelenght))
        # from io import BytesIO 

        # if you have an image or anything that saves to a stream
        buffer = BytesIO()
        img.save(buffer, "png")  # 'save' function for PIL, adapt as necessary
        buffer.seek(0)

        await ctx.send(file=discord.File(fp=buffer, filename="whatever.png"))
    
    


def setup(bot):
    bot.add_cog(physics(bot))
