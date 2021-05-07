import discord
from discord.ext import commands
import asyncio
from textwrap import wrap


# ! MESS 


DNAGeneticCodeDict = {
    "AAA": "Phe",
    "AAG": "Phe",

    "AAT": "Leu",
    "AAC": "Leu",
    "GAA": "Leu",
    "GAG": "Leu",
    "GAT": "Leu",
    "GAC": "Leu",

    "AGA": "Ser",
    "AGG": "Ser",
    "AGT": "Ser",
    "AGC": "Ser",
    "TCA": "Ser",
    "TCG": "Ser",

    "GGA": "Pro",
    "GGG": "Pro",
    "GGT": "Pro",
    "GGC": "Pro",

    "TAA": "Ile",
    "TAG": "Ile",
    "TAT": "Ile",

    "TAC": "Met",

    "TGA": "Thr",
    "TGG": "Thr",
    "TGT": "Thr",
    "TGC": "Thr",

    "CAA": "Val",
    "CAG": "Val",
    "CAT": "Val",
    "CAC": "Val",

    "CGA": "Ala",
    "CGG": "Ala",
    "CGT": "Ala",
    "CGC": "Ala",

    "ACA": "Cys",
    "ACG": "Cys",

    "ACC": "Trp",

    "ATA": "Tyr",
    "ATG": "Tyr",

    "ATT": "STP",
    "ATC": "STP",
    "ACT": "STP",

    "GCA": "Arg",
    "GCG": "Arg",
    "GCT": "Arg",
    "GCC": "Arg",
    "TCT": "Arg",
    "TCC": "Arg",

    "GTA": "His",
    "GTG": "His",

    "GTT": "Gln",
    "GTC": "Gln",

    "TTA": "Asn",
    "TTG": "Asn",

    "TTT": "Lys",
    "TTC": "Lys",

    "CCA": "Gly",
    "CCG": "Gly",
    "CCT": "Gly",
    "CCC": "Gly",

    "CTA": "Asp",
    "CTG": "Asp",

    "CTT": "Glu",
    "CTC": "Glu"

}

RNAGeneticCodeDict = {
    "UUU": "Phe",
    "UUC": "Phe",

    "UUA": "Leu",
    "UUG": "Leu",
    "CUU": "Leu",
    "CUC": "Leu",
    "CUA": "Leu",
    "CUG": "Leu",

    "UCU": "Ser",
    "UCC": "Ser",
    "UCA": "Ser",
    "UCG": "Ser",
    "AGU": "Ser",
    "AGC": "Ser",

    "CCU": "Pro",
    "CCC": "Pro",
    "CCA": "Pro",
    "CCG": "Pro",

    "AUU": "Ile",
    "AUC": "Ile",
    "AUA": "Ile",

    "AUG": "Met",

    "ACU": "Thr",
    "ACC": "Thr",
    "ACA": "Thr",
    "ACG": "Thr",

    "GUU": "Val",
    "GUC": "Val",
    "GUA": "Val",
    "GUG": "Val",

    "GCU": "Ala",
    "GCC": "Ala",
    "GCA": "Ala",
    "GCG": "Ala",

    "UGU": "Cys",
    "UGC": "Cys",

    "UGG": "Trp",

    "UAU": "Tyr",
    "UAC": "Tyr",

    "UAA": "STP",
    "UAG": "STP",
    "UGA": "STP",

    "CGU": "Arg",
    "CGC": "Arg",
    "CGA": "Arg",
    "CGG": "Arg",
    "AGA": "Arg",
    "AGG": "Arg",

    "CAU": "His",
    "CAC": "His",

    "CAA": "Gln",
    "CAG": "Gln",

    "AAU": "Asn",
    "AAC": "Asn",

    "AAA": "Lys",
    "AAG": "Lys",

    "GGU": "Gly",
    "GGC": "Gly",
    "GGA": "Gly",
    "GGG": "Gly",

    "GAU": "Asp",
    "GAC": "Asp",

    "GAA": "Glu",
    "GAG": "Glu"

}

def DNA_RNA_Decoder(sequence_string, seqtype):
    cdn = (sequence_string.upper()).replace(" ", "")
    cdnlst = wrap(cdn, 3)
    aminoacid_lst = []

    if seqtype == "DNA":
        for i in cdnlst:
            aminoacid_lst.append(DNAGeneticCodeDict.get(i, i))
        # print(aminoacid_lst)
        return aminoacid_lst

    if seqtype == "RNA":
        for i in cdnlst:
            aminoacid_lst.append(RNAGeneticCodeDict.get(i, i))
        # print(aminoacid_lst)
        return aminoacid_lst



# ! MESS 


AminoDict = {
    "Alanine":  "Ala",
    "Cysteine": "Cys",
    "Aspartic acid":    "Asp",
    "Glutamic acid":    "Glu",
    "Phenylalanine":    "Phe",
    "Glycine":  "Gly",
    "Histidine":   "His",
    "Isoleucine":   "Ile",
    "Lysine":   "Lys",
    "Leucine":  "Leu",
    "Methionine":   "Met",
    "Asparagine":   "Asn",
    "Pyrrolysine":  "Pyl",
    "Proline":  "Pro",
    "Glutamine":    "Gln",
    "Arginine": "Arg",
    "Serine":   "Ser",
    "Threonine":    "Thr",
    "Selenocysteine":   "Sec",
    "Valine":   "Val",
    "Tryptophan":   "Trp",
    "Tyrosine": "Tyr"
}

CodonDict = {
    "ala":  "Alanine",
    "cys":  "Cysteine",
    "asp":  "Aspartic acid",
    "glu":  "Glutamic acid",
    "phe":  "Phenylalanine",
    "gly":  "Glycine",
    "his":  "Histidine",
    "ile":  "Isoleucine",
    "lys":  "Lysine",
    "leu":  "Leucine",
    "met":  "Methionine",
    "asn":  "Asparagine",
    "pyl":  "Pyrrolysine",
    "pro":  "Proline",
    "gln":  "Glutamine",
    "arg":  "Arginine",
    "ser":  "Serine",
    "thr":  "Threonine",
    "sec":  "Selenocysteine",
    "val":  "Valine",
    "trp":  "Tryptophan",
    "tyr":  "Tyrosine",

    "stp":  "stp"
}



# RNAGeneticCodeDict = {
#     []: "",
#     []: "",
#     []: ""
# }


def codon_translator(codon_string):
    cdn = (codon_string.lower()).replace(" ", "")
    cdnlst = wrap(cdn, 3)
    trans_lst = []
    for i in cdnlst:
        trans_lst.append(CodonDict.get(i, i))
    # print(trans_lst)
    return trans_lst





class aminoacids(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded aminoacids")

    @commands.command()
    async def listaminoacids(self, ctx): # list amiinoacids
        embed = discord.Embed(
        colour=discord.Colour(0x3b12ef),
        description="Wikipedia:",
        )

        embed.set_author(
            name=f"Amino Acids list",
            url=f"https://en.wikipedia.org/wiki/Proteinogenic_amino_acid", 
            icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png" # ! edit
            )
        embed.set_footer(
            text=f"{self.bot.thanks()}",
            icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
            )

        for acid, code in AminoDict.items():
            embed.add_field(
                name=acid,
                value=code
                )
            
        await ctx.send(content="", embed=embed)



    @commands.command()
    async def translateaminoacids(self, ctx, *, sequence_unfiltered): # list amiinoacids
        sequence = discord.utils.escape_mentions(sequence_unfiltered)
        newseq = codon_translator(sequence)
        newseqstr = ' '.join([str(elem) for elem in newseq])
        if len(newseqstr) >= 1900:
            await ctx.send("The genetic code is too big to fit in 1 message")
            return
        await ctx.send(newseqstr)

    #! add easter egggs !
    @commands.command()
    async def decodegeneticcode(self, ctx, *, sequence_unfiltered): # list amiinoacids
        sequence = discord.utils.escape_mentions(sequence_unfiltered)
        seqtype = None
        if "u" in sequence.lower() and "t" in sequence.lower(): #fucks with me
            await ctx.send("is this DNA or RNA or troll?")
            return
        if "u" in sequence.lower(): #RNA mode
            seqtype = "RNA"
        elif "t" in sequence.lower(): # DNA mode
            seqtype = "DNA"
        else:
            await ctx.send("i'm not sure if this is DNA or RNA string?")
            return

        # forbidden_letters = ['''"b", "d", "e", "f", 
        #     "h", "i", "j", "k", "l", "m", "n", "o", "p", 
        #     "q", "r", "s", "v", "w", "x", "y", "z", 
        #     "1", "2", "3", "4", "5" ,"6", "7", "8", "9",''']

        # if True:
        #     await ctx.send(f"{ctx.user.mention}, You know that DNA is made from T C G A and RNA from U C G A ?\nstop trolling, this bot won't crash")
        #     return

        newseq = DNA_RNA_Decoder(sequence, seqtype)
        newseqstr = ' '.join([str(elem) for elem in newseq])
        if len(newseqstr) >= 1900:
            await ctx.send("The genetic code is too big to fit in 1 message")
            return
        await ctx.send(newseqstr)





def setup(bot):
    bot.add_cog(aminoacids(bot))
