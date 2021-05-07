import discord
from discord.ext import commands
import asyncio
import os

def sorterfunc(x):
    b=''.join(i for i in x if i.isdigit())
    b=int(b)
    return b


class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded help")

    @commands.command()
    async def help(self, ctx, requested_page="1"):
        matti_user = self.bot.get_user(446959856318939137) #! my id
        prefix = await self.bot.get_prefix(ctx.message) # prefix
        beta_status = await self.bot.check_beta(ctx.message) # are beta functions enabled?


        # await ctx.send(f"help comming soon !\nif you still need help contact {user}")
        # await ctx.send(f"soon out of beta!")


        help_obj = []

        #! NORMAL USER

        files = os.listdir("./text_files/help_command_files") # load
        files.sort(key=sorterfunc) # sort
        
        for file in files:
            if file.endswith(".txt") and file.startswith("help"):
                with open (f"./text_files/help_command_files/{file}", "r", encoding='utf-8') as myfile:
                    content = myfile.read()\
                        .replace("@prefix@",f"{prefix}")\
                        .replace("@user@",f"{ctx.author}")\
                        .replace("@matti@",f"{matti_user}")
                    help_obj.append(content)

        #! ADMIN ONLY
        if ctx.author.guild_permissions.administrator: # check if admin
            files = os.listdir("./text_files/admin_command_files") # load
            files.sort(key=sorterfunc) # sort

            for file in files:
                if file.endswith(".txt") and file.startswith("help"):
                    with open (f"./text_files/admin_command_files/{file}", "r", encoding='utf-8') as myfile:
                        content = myfile.read()\
                            .replace("@prefix@",f"{prefix}")\
                            .replace("@user@",f"{ctx.author}")\
                            .replace("@matti@",f"{matti_user}")
                        help_obj.append(content)

        
        #! BETA ONLY
        if beta_status: # if beta is enabled
            files = os.listdir("./text_files/beta_command_files") # load
            files.sort(key=sorterfunc) # sort

            for file in files:
                if file.endswith(".txt") and file.startswith("help"):
                    with open (f"./text_files/beta_command_files/{file}", "r", encoding='utf-8') as myfile:
                        content = myfile.read()\
                            .replace("@prefix@",f"{prefix}")\
                            .replace("@user@",f"{ctx.author}")\
                            .replace("@matti@",f"{matti_user}")
                        help_obj.append(content)


        # if self.bot.verify(ctx.author.id):
        #     files = os.listdir("./text_files/premium_command_files")
        #     for file in files:
        #         if file.endswith(".txt") and file.startswith("help"):
        #             with open (f"./text_files/premium_command_files/{file}", "r", encoding='utf-8') as myfile:
        #                 content = myfile.read()\
        #                     .replace("@user@",f"{ctx.author}")\
        #                     .replace("@matti@",f"{matti_user}")
        #                 help_obj.append(content)


        timeout_time = 60 # 1 min


        pages = len(help_obj)

        if requested_page.isnumeric(): #* is whatever someone entered an int?

            if int(requested_page) < 1: #* if it's smaller then 1 set it to 1
                cur_page = 1

            elif int(requested_page) > pages: #* if it's bigger than number of pages
                cur_page = pages #* set it to max

            else: #* it's a number between min and max
                cur_page = int(requested_page) #* set the page to whatever user inputed
        else:
            cur_page = 1 #* it's not a number, set it to 1

        
        message = await ctx.send(f"`Page {cur_page}/{pages}:`\n\n"\
                                f"{help_obj[cur_page-1]}")
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            if reaction.message.id == message.id:
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"
            # The check on top ensures that the reaction is placed on correct message

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout_time, check=check)
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


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild == None:
            return False
        if message.author.bot:
            return False
        if f"<@{str(self.bot.user.id)}>" == str(message.content) or f"<@!{str(self.bot.user.id)}>" == str(message.content):
            prefix = await self.bot.get_prefix(message)
            await message.channel.send(f"{message.author.mention} need `{prefix}help` ?")

def setup(bot):
    bot.add_cog(help(bot))
