import discord
from discord.ext import commands
import asyncio

yes = "<:yes:632256160153468929>"
no = "<:no:632256159981502504>"
proton_symbol = "Ⓟ⁺"
electron_symbol = "Ⓔ⁻"
neutron_symbol = "Ⓝ⁰"

import chemlib

class chemistry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded chemistry")

    @commands.command()
    async def sayyy(self, ctx, word):
        await ctx.send(word)

    @commands.command()
    async def element(self, ctx, ele):
        try:
            element = chemlib.Element(ele.lower().capitalize()) #Instantiate with symbol of Element
        except:
            await ctx.send("Requested element not found\n try e.g. Cu")
            return

        # if element.properties.get('Discoverer') and element.properties.get('Year') != "Unknown":
        #     description = \
        #         f"Discovered by {element.properties.get('Discoverer')} "\
        #         f"in {element.properties.get('Year')}"
        # elif element.properties.get('Discoverer'):
        #     description = \
        #         f"Discovered by {element.properties.get('Discoverer')}"
        # elif element.properties.get('Year') != "Unknown":
        #     description = \
        #         f"in {element.properties.get('Year')}"
        # else:
        #     description = \
        #         "Discovery info not found"

        # print(description)


        embed = discord.Embed(
            title=\
                f"{int(element.properties.get('AtomicNumber'))} - "\
                f"**{element.properties.get('Element')}** "\
                f"({element.properties.get('Symbol')})",
            colour=discord.Colour(0x3b12ef),
            # url="https://discordapp.com/",
            description=\
                f"Discovered by {element.properties.get('Discoverer')} "\
                f"in {element.properties.get('Year')}"\
        )


        if element.properties.get("Radioactive"):
            embed.add_field(
            name="☢️?",
            value=yes,
            inline=True
            )
        else:
            embed.add_field(
            name="☢️?",
            value=no,
            inline=True
            )

        if element.properties.get("Natural"):
            embed.add_field(
            name="Natural?",
            value=yes,
            inline=True
            )
        else:
            embed.add_field(
            name="Natural?",
            value=no,
            inline=True
            )

        if element.properties.get("Metal"):
            embed.add_field(
            name="Type?",
            value=f"Metal\n({element.properties.get('Type')})",
            inline=True
            )

        if element.properties.get("Nonmetal"):
            embed.add_field(
            name="Type?",
            value=f"Non-Metal\n({element.properties.get('Type')})",
            inline=True
            )
            
        if element.properties.get("Metalloid"):
            embed.add_field(
            name="Type?",
            value=f"Metalloid\n({element.properties.get('Type')})",
            inline=True
            )

        embed.add_field(
        name="Phase?",
        value=\
            f"{element.properties.get('Phase').capitalize()} at room temperature\n"\
            f"Melting Point: {element.properties.get('MeltingPoint')}\n"\
            f"Boiling Point: {element.properties.get('BoilingPoint')}\n"\
            f"Density: {element.properties.get('Density')}g/cm³\n",
            inline=False
            )

        embed.add_field(
        name="Contains?",
        value=\
            f"{int(element.properties.get('Neutrons'))} {neutron_symbol}\n"\
            f"{int(element.properties.get('Protons'))} {proton_symbol}\n"\
            f"{int(element.properties.get('Electrons'))} {electron_symbol}\n",
            inline=False
            )

        embed.add_field(
        name="Location on Periodic Table?",
        value=\
            f"{int(element.properties.get('Period'))} - Period\n"\
            f"{int(element.properties.get('Group'))} - Group\n",
            inline=False
            )



        # embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/1.png")
        embed.set_author(
            name=ctx.bot.user.display_name,
            icon_url=ctx.bot.user.avatar_url
        )
        embed.set_footer(
            text=f"{self.bot.thanks()}",
            icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
        )

        # embed.add_field(
        #     name="field title",
        #     value="some of these properties have different limits."
        # )
        # embed.add_field(
        #     name="another field title",
        #     value="try exceeding some of them! (coz idk them)"
        # )
        # embed.add_field(
        #     name=":thinking: this supports emotes! (and custom ones too)",
        #     value="if you exceed them, the error will tell you which value exceeds it."
        # )
        # embed.add_field(
        #     name="Inline",
        #     value="these last two fields",
        #     inline=True
        # )
        # embed.add_field(
        #     name="Fields",
        #     value="are inline fields",
        #     inline=True
        # )

        await ctx.send(embed=embed)






    # @commands.command(aliases = ["getmolarmass"])
    # async def getmm(self, ctx, comp):
    #     try:
    #         comp = chemlib.Element(comp.lower().capitalize()) #Instantiate with symbol of Element
    #     except:
    #         await ctx.send("Requested compound not found\n try e.g. H2O")
    #         return





def setup(bot):
    bot.add_cog(chemistry(bot))
