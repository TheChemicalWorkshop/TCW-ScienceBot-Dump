import discord
from discord.ext import commands
import asyncio

import ast
import subprocess


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)



devs = [446959856318939137] # ! my bot 589968097369128966

def dev_check(ctx):
    return str(ctx.author.id) in str(devs)
    
class tcw_management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded tcw_management")


    @commands.command()
    @commands.check(dev_check)
    async def execute(self, ctx, *, cmd):

        if ctx.author.id not in devs:
            return

        """Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
        - `bot`: the bot instance
        - `discord`: the discord module
        - `commands`: the discord.ext.commands module
        - `ctx`: the invokation context
        - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating
        >eval ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        if result == None:
            return
        await ctx.send(result)

    @commands.command()
    @commands.check(dev_check)
    async def runlinux(self, ctx, *cmd):
        cmd_list = list(cmd)
        result = subprocess.run(cmd_list, stdout=subprocess.PIPE)
        print(result.stdout.decode('UTF-8'))
        await ctx.send(result.stdout.decode('UTF-8'))
        
        # import subprocess
        # MyOut = subprocess.Popen(cmd_list, 
        #             stdout=subprocess.PIPE, 
        #             stderr=subprocess.STDOUT)
        # stdout,stderr = MyOut.communicate()
        # print(stdout)
        # print(stderr)


    @commands.command() #! only admin
    @commands.has_permissions(administrator=True)
    async def blacklists(self, ctx):
        end_string = ""
        blacklists = self.bot.blacklists
        for user in blacklists:
            end_string += f"<@{user.get('discord_id')}> is blacklisted for **{', '.join(user.get('reasons'))}**\n"
        if end_string:
            if len(end_string) > 1900:
                await ctx.send(f"Cannot show you {len(blacklists)} Blacklists\nContact TCW for a full list")
            await ctx.send(end_string)
        else:
            await ctx.send("no one is blacklisted")
            return
    
    @commands.command() #! only admin
    @commands.has_permissions(administrator=True)
    async def tcwban(self, ctx):

        if ctx.guild is False: return
        blacklists = self.bot.blacklists
        message = await ctx.send(f"You are about to ban {len(blacklists)} People, TCW recommends this.\n\nType **YES** to ban them pernamently !")

        def pred(m):
            if m.author.id == ctx.author.id:
                return True
            else:
                return False
    
        try:
            msg = await self.bot.wait_for('message', check=pred, timeout=60.0)
            #print(msg.channel.id)
        except asyncio.TimeoutError:
            await message.edit(content='Timed out ?')
            return
        else:
            if msg.content.lower() == "yes":
                # ! WE ARE BANING !
                # cuntclass
                class Cunt(object):
                    id = 0
                    created_at = 0

                    # The class "constructor" - It's actually an initializer 
                    def __init__(self, id, created_at):
                        self.id = id
                        self.created_at = created_at
                #cuntmaker
                def make_cunt(id, created_at):
                    cunt = Cunt(id, created_at)
                    return cunt

                end_string = ""

                for user in blacklists:
                    end_string += f"Successfully banned <@{user.get('discord_id')}> for **{', '.join(user.get('reasons'))}**\n"
                    newcnt = make_cunt(user.get('discord_id'), 0)
                    await ctx.guild.ban(newcnt, reason=', '.join(user.get('reasons')))
                if len(end_string) > 1900:
                    await message.edit(content=f"Successfully banned {len(blacklists)} users")

                await message.edit(content=end_string)
            # ? Trolls and easterggs ----
            elif msg.content.lower() == "no":
                await message.edit(content='😞')
                return
            elif msg.content.lower() == "maybe":
                await message.edit(content=f'Decide {msg.author.mention} ffs')
                return
            elif msg.content.lower() == "gay":
                await message.edit(content=f'Yes you {msg.author.mention}')
                return
            elif msg.content.lower() == "ban":
                await message.edit(content='To ban, you should have anwsered yes')
                return
            else:
                await message.edit(content='?\nYour anwser must be either **yes** or no')
                return

    @tcwban.error
    async def tcwban_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            if error.original.text == "Missing Permissions":
                await ctx.send("I need Permissions to run this command ! gimme admin")
                print("test")
                return
            await ctx.send(error)
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return
        else:
            print(error)
            print(ctx.guild.id)




def setup(bot):
    bot.add_cog(tcw_management(bot))
