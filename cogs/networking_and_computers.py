import discord
from discord.ext import commands
import asyncio

import socket

# import nmap3

from PIL import Image
import glob, os

import codecs

import lists.css_colors as css_colors

# https://github.com/ipinfo/python

max_ping_count_free = 5
max_ping_count_premium = 100

yellow = "<:sipp:657282746384646170>" 

from pythonping import ping

class networking_and_computers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded networking_and_computers")


    @commands.command()
    async def hosttoip(self, ctx, host):
        try:
            ip = socket.gethostbyname(host)
        except:
            await ctx.send("error, host invalid?")
            return
        await ctx.send(ip)

    @commands.command()
    async def pingserver(self, ctx, ip, count = 2):
        #!
        #! add anti @everyone ping
        #!

        if count == 0:
            await ctx.reply(f"{yellow} - count 0?")
            return

        premium = False    

        for donator in self.bot.donators:
            if \
                ctx.author.id == donator.get("discord_id") or \
                ctx.guild.owner_id == donator.get("discord_id"):
                    premium = True

        if "@" in ctx.message.content:
            return

        if not premium:
            if count > max_ping_count_free:
                await ctx.send(\
                    f"you can't have more than {max_ping_count_free} pings\n"\
                    f"upgrade to premium for {max_ping_count_premium} pings")
                return
        if premium:
            if count > max_ping_count_premium:
                await ctx.send(f"sorry, you can't have more than {max_ping_count_premium} pings :(")
                return


        try:
            response_list = ping(ip, count=count)
        except RuntimeError as err:
            await ctx.send(err)
            return
        except Exception as err:
            await ctx.send("you found a bug? you are not supposed to see this message!")
            print(err)
            return

        await ctx.send(\
            f"min ping - {response_list.rtt_min_ms}ms\n"\
            f"**average ping - {response_list.rtt_avg_ms}ms**\n"\
            f"max ping - {response_list.rtt_max_ms}ms\n\n"\
            f"packet loss - {response_list.packet_loss}%")
        # print(response_list.rtt_avg_ms)
        # print(response_list.packet_loss)

    # @commands.command()
    # async def nmap(self, ctx, host):
    #     nmap = nmap3.Nmap()
    #     results = nmap.scan_top_ports(host, args="–p 8080")
    #     rtl = list(results.keys())
    #     rtl.remove("stats")
    #     rtl.remove("runtime")
    #     # print(results)
    #     for result in rtl:
    #         send_string = ""
    #         res = results.get(result)

    #         for host in res.get("hostname"):
    #             send_string += f"name - {host.get('name')}\n"
    #             send_string += f"type - {host.get('type')}\n\n"
            
    #         for port in res.get("ports"):
    #             send_string += f"Protocol - {port.get('protocol')}\n"
    #             send_string += f"Port - {port.get('portid')}\n"
    #             send_string += f"Status - {port.get('reason')}\n\n"
    #         send_string += f"------------------"
    #         await ctx.send(send_string)

    @commands.command()
    async def css_color(self, ctx, *, color):

        filtered_color = color.replace(" ", "").lower()

        clr = css_colors.css_color_names.get(filtered_color)
        if not clr:
            await ctx.reply("your color cannot be recognised by CSS")
            return


        rgb_color = (tuple(int(clr.strip("#")[i:i+2], 16) for i in (0, 2, 4)))


        img = Image.new('RGB', (1024, 1024), color = rgb_color)
        # img.save('pil_color.png')

        from io import BytesIO 

        # if you have an image or anything that saves to a stream
        buffer = BytesIO()
        img.save(buffer, "png")  # 'save' function for PIL, adapt as necessary
        buffer.seek(0)

        await ctx.send(content = f"{filtered_color} - {clr.upper()}", file=discord.File(fp=buffer, filename="whatever.png"))
    

    @commands.command()
    async def gencolor(self, ctx, r_in_hex_in, g_in = None, b_in = None):

        if g_in and not b_in:
            await ctx.send("ERROR, you need R G B value like this:\n"\
                f"{ctx.prefix}{ctx.command.name} 0 49 83")
            return

        if g_in == None:
            #rgb mode
            rgb_color = (tuple(int(r_in_hex_in[i:i+2], 16) for i in (0, 2, 4)))
        else:
            try:
                r = int(r_in_hex_in)
                g = int(g_in)
                b = int(b_in)
                rgb_color = (r, g, b)
            except Exception as err:
                await ctx.send("ERROR?")
                return

        img = Image.new('RGB', (1024, 1024), color = rgb_color)
        # img.save('pil_color.png')

        from io import BytesIO 

        # if you have an image or anything that saves to a stream
        buffer = BytesIO()
        img.save(buffer, "png")  # 'save' function for PIL, adapt as necessary
        buffer.seek(0)

  

        await ctx.send(file=discord.File(fp=buffer, filename="whatever.png"))
    
  


def setup(bot):
    bot.add_cog(networking_and_computers(bot))
