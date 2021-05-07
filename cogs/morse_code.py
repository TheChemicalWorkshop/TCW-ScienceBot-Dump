from inspect import FullArgSpec
import discord
from discord.ext import commands
import asyncio
from pydub import AudioSegment # to export

import random
import string

import os

morse_dot = AudioSegment.from_file("./media/audio/morse_code/dot.wav", format="wav")
morse_dash = AudioSegment.from_file("./media/audio/morse_code/dash.wav", format="wav")
morse_letter_space = AudioSegment.from_file("./media/audio/morse_code/letter_space.wav", format="wav")
morse_symbol_space = AudioSegment.from_file("./media/audio/morse_code/symbol_space.wav", format="wav")
morse_word_space = AudioSegment.from_file("./media/audio/morse_code/word_space.wav", format="wav")


def randomStringDigits(stringLength=10):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_uppercase + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def to_morse(input):
    morse_sting = ""
    for i in input:
        x = CODE.get(i.upper())
        if x:
            morse_sting += f"{x} "
    return morse_sting

def convert_and_filter(input):
    output = ""
    for word in input:
        for i in word:
            if CODE.get(i.upper()):
                output += i.upper()
        if output[-1] != " ":
            output += " "
    output += " " # space for next word
    return output

def encode_morse_sound(text):
    combined = AudioSegment.empty() # start
    # combined = morse_word_space # must be empty
    last_character = ""
    ignore = False
    for i in text:
        if i == ".":
            if last_character == "." or last_character == "-":
                combined = combined + morse_symbol_space
            elif last_character == " ":
                if ignore:
                    ignore = False
                else:
                    combined = combined + morse_letter_space
            combined = combined + morse_dot
        elif i == "-":
            if last_character == "." or last_character == "-":
                combined = combined + morse_symbol_space
            elif last_character == " ":
                if ignore:
                    ignore = False
                else:
                    combined = combined + morse_letter_space
            combined = combined + morse_dash
        elif i == "|":
            if last_character == " " and i == "|":
                combined = combined + morse_word_space
                ignore = True
        elif i == " ":
            pass
        else:
            return None
        last_character = i

    return combined
#.--. .- .-. .. ... | 
#! The length of a dot is 1 time unit.
#! A dash is 3 time units.
#! The space between symbols (dots and dashes) of the same letter is 1 time unit.
#! The space between letters is 3 time units.
#! The space between words is 7 time units.

#'N': '-.'
#
# . = . (1)
# - = - (3)
# , = (space 1)
# " " = (space 3)
# | = (space 7)
#
# NN N N
# -,. -,.|-,.|-,.


# ` ` (a space) = 3 units
# `|` = 1 unit
# ` | ` (space, pipe, space) = 7 units
# `` (no space left or right) = 1 unit
# `.` = 1 unit
# `-` = 3 units



CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',   ' ': '|',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }

CODE_REVERSED = {value:key for key,value in CODE.items()}



class morse_code(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded morse_code")


    @commands.command()
    async def encryptmorse(self, ctx, *unfiltered_test):


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
        

        text = (convert_and_filter(unfiltered_test))[:-1]

        out = to_morse(text)

        if len(out) > 1000:
            await ctx.send(f"sorry, your output is too long :(")
            return

        if not out:
            await ctx.send("could not be encoded? use A-Z 0-9")
            return

        if not premium:
            await ctx.send(content = f"{text}\n\n`{out}`")

        else: #!preimum
            # await ctx.send(content = f"{text}\n\n`{out}`")
            sound = encode_morse_sound(out)
            morse_id = str(randomStringDigits(10))
            file_handle = sound.export(f"./output/{morse_id}.wav", format="wav")
            await ctx.send(content = f"{text}\n\n`{out}`", file=discord.File(f'./output/{morse_id}.wav'))
            
            file_handle.close()
            if os.path.exists(f"./output/{morse_id}.wav"):
                os.remove(f"./output/{morse_id}.wav")
            else:
                print(f"./output/{morse_id}.wav - something broke") 
            

def setup(bot):
    bot.add_cog(morse_code(bot))
