import discord
from discord.ext import commands
import asyncio
import os

import json

class bot_settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded bot_settings")

    @commands.has_permissions(administrator=True)
    @commands.group(invoke_without_command=True)
    async def settings(self, ctx):
        matti_user = self.bot.get_user(446959856318939137) #! my id

        prefix = await self.bot.get_prefix(ctx)


        premium = self.bot.verify(ctx.author.id)

        help_obj = []

        files = os.listdir("./text_files/settings_command_files")
        for file in files:
            if file.endswith(".txt") and file.startswith("help"):
                with open (f"./text_files/settings_command_files/{file}", "r") as myfile:
                    content = myfile.read()\
                        .replace("@prefix@",f"{prefix}")
                    help_obj.append(content)

        pages = len(help_obj)
        cur_page = 1
        message = await ctx.send(f"`Page {cur_page}/{pages}:`\n\n"\
                                f"{help_obj[cur_page-1]}")
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check) #* a minute
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(content=f"`Page {cur_page}/{pages}:`\n\n"\
                                f"{help_obj[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(content=f"`Page {cur_page}/{pages}:`\n\n"\
                                f"{help_obj[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds
                


    #! --------- PREFIX ----------------          
    @commands.has_permissions(administrator=True)
    @settings.command()
    async def prefix(self, ctx, pfx=None):
        if not pfx:
            await ctx.send("you need to specify a prefix\n"\
                f"like this: `{ctx.prefix}{ctx.invoked_with} $`")
            return
        with open("settings_files/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[(str(ctx.guild.id))] = pfx

        with open("settings_files/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        prefix = await self.bot.get_prefix(ctx)
        await ctx.send(f"your new prefix: `{prefix}`")




    #! --------- BETA FUNCTIONS ----------------          
    @commands.has_permissions(administrator=True)
    @settings.command()
    async def enable_beta(self, ctx, optin=None):
        if not optin:
            beta_optin_status = await self.bot.check_beta(ctx)
            if optin:
                await ctx.send("Server is set to beta, beta functions are enabled")
            if not optin:
                await ctx.send("Server isn't beta, beta functions are not enabled")
            return
        if optin.lower() == "yes" or optin.lower() == "no":
            with open("settings_files/beta_optin.json", "r") as f:
                beta_optin = json.load(f)

            if optin.lower() == "yes":
                beta_optin[(str(ctx.guild.id))] = True
            if optin.lower() == "no":
                beta_optin[(str(ctx.guild.id))] = False

            with open("settings_files/beta_optin.json", "w") as f:
                json.dump(beta_optin, f, indent=4)

            beta_optin_status = await self.bot.check_beta(ctx)
            await ctx.send(f"your optin is: `{optin}`")
        else:
            await ctx.send("so... *yes* or *no* ?")

def setup(bot):
    bot.add_cog(bot_settings(bot))
