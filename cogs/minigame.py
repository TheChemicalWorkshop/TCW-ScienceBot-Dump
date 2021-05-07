import discord
from discord.ext import commands, tasks
import asyncio
import random
import aiosqlite

# ! add feature to change price
# ! add premium to chnage per role price

import datetime
time_format = "%Y-%m-%dT%H:%M:%S"


local_db = "main.db"

devs = [446959856318939137, 589968097369128966] # ! my bot 589968097369128966

# minigame_shop_allowed = [653280037793038366, 644966555930853390, 710976715756929106]
minigame_shop_roles = ["red", "yellow", "white", "pink", "orange", "purple", "green", "gray", "blue", "cyan"]



def dev_check(ctx):
    return str(ctx.author.id) in str(devs)



#* --------- creates tables ---------
async def create_table_minigame_settings(name):
    conn = await aiosqlite.connect(name)
    c = await conn.cursor()

    await c.execute(f'CREATE TABLE minigame_settings ( guild_id integer, enabled BOOLEAN, role_price integer ); ')
    await conn.commit()

    await conn.close()
async def create_table_role_settings(name):
    conn = await aiosqlite.connect(name)
    c = await conn.cursor()

    await c.execute(f'CREATE TABLE role_settings ( guild_id integer, discord_id integer, role_id integer, expiration_date smalldatetime ); ')
    await conn.commit()

    await conn.close()
#* --------- creates tables ---------







async def optin_create_server(guild_id): # ? creates server, only for internal use
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    await c.execute(f'INSERT INTO minigame_settings VALUES ({guild_id}, False, 500)') # adds server to the db, enabled 1
    await conn.commit()

    await conn.close()


async def add_user_role_to_db(guild_id, discord_id, role_id, expiration_date): # ? creates server, only for internal use
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()
    # ? adds guild, user, role and date to the database
    await c.execute(f'INSERT INTO role_settings VALUES ({guild_id}, {discord_id}, {role_id}, \'{expiration_date}\')')
    await conn.commit()

    await conn.close()

async def delete_user_role_from_db(guild_id, discord_id, role_id):
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    try:
        await c.execute(f'DELETE FROM role_settings \
        WHERE guild_id = {guild_id} \
        AND discord_id = {discord_id} \
        AND role_id = {role_id};') # ? remove user
    except Exception as err:
        pass

    await conn.commit()
    await conn.close()

async def list_all_active_roles_db(): # ? creates server, only for internal use
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()
    # ? adds guild, user, role and date to the database
    await c.execute(f'SELECT * FROM role_settings')
    await conn.commit()

    result = await c.fetchall()

    await conn.close()
    return result






async def optin_check(guild_id): # ? checks if true/false, if does not exists, creates new

    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    await c.execute(f'SELECT enabled FROM minigame_settings WHERE guild_id={guild_id}') # ? get points
    await conn.commit()

    result = await c.fetchone()
    if result == None:
        await optin_create_server(guild_id)
        await c.execute(f'SELECT enabled FROM minigame_settings WHERE guild_id={guild_id}') # ? get points
        await conn.commit()
        result = await c.fetchone()

    await conn.close()
    if result[0] == 0:
        return False
    if result[0] == 1:
        return True

async def optin_change(guild_id, enabled): # ? changes optin to enabled=smth
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    try:
        await c.execute(f'UPDATE minigame_settings SET enabled = {enabled} WHERE guild_id = {guild_id};') # ? add points
    except Exception as err:
        print(err)
    await conn.commit()

    await conn.close()





async def createplayer(discord_id):
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    await c.execute(f'INSERT INTO minigame VALUES ({discord_id}, 0)') # ? add player with points 0
    await conn.commit()

    await conn.close()

async def deleteplayer(discord_id):
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    try:
        await c.execute(f'DELETE FROM minigame WHERE discord_id = {discord_id};') # ? remove user
    except Exception as err:
        pass

    await conn.commit()
    await conn.close()


async def addpoints(discord_id, points):
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    try:
        await c.execute(f'UPDATE minigame SET points = {points} WHERE discord_id = {discord_id};') # ? add points
    except Exception as err:
        print(err)
    await conn.commit()

    await conn.close()

async def mypoints(discord_id):
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    await c.execute(f'SELECT points FROM minigame WHERE discord_id={discord_id}') # ? get points
    await conn.commit()

    result = await c.fetchone()
    if result == None:
        await createplayer(discord_id)
        await c.execute(f'SELECT points FROM minigame WHERE discord_id={discord_id}') # ? get points
        await conn.commit()
        result = await c.fetchone()


    await conn.close()
    return result[0]

async def allpoints():
    conn = await aiosqlite.connect(local_db)
    c = await conn.cursor()

    await c.execute(f'SELECT * FROM minigame') # ? get points
    await conn.commit()

    result = await c.fetchall()


    await conn.close()
    return result



compounds = {"Aluminium antimonide": "AlSb",
    "Aluminium arsenide": "AlAs",
    "Aluminium nitride": "AlN",
    "Aluminium oxide": "Al2O3",
    "Aluminium phosphide": "AlP",
    "Aluminium chloride": "AlCl3",
    "Aluminium fluoride": "AlF3",
    "Aluminium hydroxide": "Al(OH)3",
    "Aluminium nitrate": "Al(NO3)3",
    "Aluminium sulfate": "Al2(SO4)3",
    "Ammonia": "NH3",
    "Ammonium azide": "NH4N3",
    "Ammonium bicarbonate": "NH4HCO3",
    "Ammonium chromate": "(NH4)2CrO4",
    "Ammonium cerium(IV) nitrate": "(NH4)2Ce(NO3)6",
    "Ammonium chloride": "NH4Cl",
    "Ammonium chlorate": "NH4ClO3",
    "Ammonium cyanide": "NH4CN",
    "Ammonium dichromate": "(NH4)2Cr2O7",
    "Ammonium hydroxide": "NH4OH",
    "Ammonium hexachloroplatinate": "(NH4)2(PtCl6)",
    "Ammonium nitrate": "NH4NO3",
    "Ammonium sulfide": "(NH4)2S4",
    "Ammonium sulfite": "(NH4)2SO3",
    "Ammonium sulfate": "(NH4)2SO4",
    "Ammonium persulfate": "(NH4)2S2O8",
    "Ammonium perchlorate": "NH4ClO4",
    "Ammonium tetrathiocyanatodiamminechromate(III)": "NH4[Cr(SCN)4(NH3)2]",
    "Antimony hydride": "SbH3",
    "Antimony pentachloride": "SbCl5",
    "Antimony pentafluoride": "SbF5",
    "Antimony trioxide": "Sb2O3",
    "Arsine": "AsH3",
    "Arsenic trioxide (Arsenic(III) oxide)": "As2O3",
    "Arsenous acid": "As(OH)3",
    "Barium azide": "Ba(N3)3",
    "Barium chloride": "BaCl2",
    "Barium chromate": "BaCrO4",
    "Barium chlorate": "BaClO3",
    "Barium carbonate": "BaCO3",
    "Barium hydroxide": "Ba(OH)2",
    "Barium iodide": "BaI2",
    "Barium nitrate": "Ba(NO3)2",
    "Barium sulfate": "BaSO4",
    "Barium fluoride": "BaF2",
    "Barium ferrite": "BaFe2O4",
    "Barium ferrate": "BaFeO4",
    "Barium titanate": "BaTiO3",
    "Barium oxide": "BaO",
    "Barium peroxide": "BaO2",
    "Beryllium bromide": "BeBr2",
    "Beryllium carbonate": "BeCO3",
    "Beryllium chloride": "BeCl2",
    "Beryllium fluoride": "BeF2",
    "Beryllium hydride": "BeH2",
    "Beryllium hydroxide": "Be(OH)2",
    "Beryllium iodide": "BeI2",
    "Beryllium nitrate": "Be(NO3)2",
    "Beryllium nitride": "Be3N2",
    "Beryllium oxide": "BeO",
    "Beryllium sulfate": "BeSO4",
    "Beryllium sulfite": "BeSO3",
    "Beryllium borohydride": "Be(BH4)2",
    "Beryllium telluride": "BeTe",
    "Bismuth(III) oxide": "Bi2O3",
    "Bismuth(III) telluride": "Bi2Te3",
    "Borax": "Na2B4O7·10H2O",
    "Boric acid": "H3BO3",
    "Boron carbide": "B4C",
    "Boron nitride": "BN",
    "Boron oxide": "B2O3",
    "Boron suboxide": "B6O",
    "Boron trichloride": "BCl3",
    "Boron trifluoride": "BF3",
    "Bromine pentafluoride": "BrF5",
    "Bromine trifluoride": "BrF3",
    "Bromine monochloride": "BrCl",
    "Cacodylic acid": "(CH3)2AsO2H",
    "Cadmium arsenide": "Cd3As2",
    "Cadmium bromide": "CdBr2",
    "Cadmium chloride": "CdCl2",
    "Cadmium fluoride": "CdF2",
    "Cadmium iodide": "CdI2",
    "Cadmium nitrate": "Cd(NO3)2",
    "Cadmium selenide": "CdSe",
    "Cadmium sulfate": "CdSO4",
    "Cadmium telluride": "CdTe",
    "Caesium bicarbonate": "CsHCO3",
    "Caesium carbonate": "Cs2CO3",
    "Caesium chromate": "Cs2CrO4",
    "Caesium chloride": "CsCl",
    "Caesium fluoride": "CsF",
    "Caesium hydride": "CsH",
    "Calcium carbide": "CaC2",
    "Calcium chlorate": "Ca(ClO3)2",
    "Calcium chloride": "CaCl2",
    "Calcium chromate": "CaCrO4",
    "Calcium cyanamide": "CaCN2",
    "Calcium fluoride": "CaF2",
    "Calcium hydride": "CaH2",
    "Calcium hydroxide": "Ca(OH)2",
    "Calcium sulfate (Gypsum)": "CaSO4",
    "Carbon dioxide": "CO2",
    "Carbon disulfide": "CS2",
    "Carbon monoxide": "CO",
    "Carbonic acid": "H2CO3",
    "Carbon tetrabromide": "CBr4",
    "Carbon tetrachloride": "CCl4",
    "Carbon tetraiodide": "CI4",
    "Carbonyl fluoride": "COF2",
    "Carbonyl sulfide": "COS",
    "Carboplatin": "C6H12N2O4Pt",
    "carborundum": "SiC",
    "Cerium(III) chloride": "CeCl3",
    "Cerium(III) bromide": "CeBr3",
    "Cerium(IV) sulfate": "Ce(SO4)2",
    "Cerium magnesium": "CeMg",
    "Cerium aluminium": "CeAl",
    "Cerium zinc": "CeZn",
    "Cerium silver": "CeAg",
    "Cerium cadmium": "CeCd",
    "Cerium mercury": "CeHg",
    "Cerium thallium": "CeTl",
    "Chloric acid": "HClO3",
    "Chlorine": "Cl2",
    "Chlorine monoxide": "ClO",
    "Chlorine dioxide": "ClO2",
    "Chlorine trioxide": "ClO3",
    "Dichlorine monoxide": "Cl2O",
    "Dichlorine dioxide": "Cl2O2",
    "Dichlorine trioxide": "Cl2O3",
    "Dichlorine tetroxide,also known as chlorine perchlorate": "ClOClO3",
    "Dichlorine hexoxide": "Cl2O6",
    "Dichlorine heptoxide": "Cl2O7",
    "Chlorine tetroxide, the peroxide": "O3ClOOClO3",
    "Chromic acid": "CrO3",
    "Chromium(III) chloride": "CrCl3",
    "Chromium(II) chloride": "CrCl2",
    "Chromium(III) oxide": "Cr2O3",
    "Chromium(IV) oxide": "CrO2",
    "Chromium(II) sulfate": "CrSO4",
    "Chromium trioxide (Chromic acid)": "CrO3",
    "Chromyl chloride": "CrO2Cl2",
    "Cisplatin (cis-platinum(II) chloride diammine)": "PtCl2(NH3)2",
    "Cobalt(II) bromide": "CoBr2",
    "Cobalt(II) chloride": "CoCl2",
    "Cobalt(II) carbonate": "CoCO3",
    "Cobalt(II) sulfate": "CoSO4",
    "Columbite": "Fe2+Nb2O6",
    "Copper(II) azide": "Cu(N3)2",
    "Copper(II) carbonate": "CuCO3",
    "Copper(I) chloride": "CuCl",
    "Copper(II) chloride": "CuCl2",
    "Copper(II) hydroxide": "Cu(OH)2",
    "Copper(II) nitrate": "Cu(NO3)2",
    "Copper(I) oxide": "Cu2O",
    "Copper(II) oxide": "CuO",
    "Copper(II) sulfate": "CuSO4",
    "Copper(I) sulfide": "Cu2S",
    "Copper(II) sulfide": "CuS",
    "Cyanogen": "(CN)2",
    "Cyanogen chloride": "CNCl",
    "Cyanuric chloride": "C3Cl3N3",
    "Cyanogen bromide": "CNBr",
    "Cyanogen iodide": "ICN",
    "Chrome-alum": "K2SO4Cr2(SO4)3.24H2O",
    "Decaborane (Diborane)": "B10H14",
    "Diammonium phosphate": "(NH4)2HPO4",
    "Diborane": "B2H6",
    "Dichlorosilane": "SiH2Cl2",
    "Digallane": "Ga2H6",
    "Dinitrogen pentoxide (nitronium nitrate)": "N2O5",
    "Dinitrogen tetroxide": "N2O4",
    "Disilane": "Si2H6",
    "Disulfur dichloride": "S2Cl2",
    "Dysprosium(III) chloride": "DyCl3",
    "Dysprosium oxide": "Dy2O3",
    "Dysprosium titanate": "Dy2Ti2O7",
    "Erbium(III) chloride": "ErCl3",
    "Europium(III) chloride": "EuCl3",
    "Erbium-copper": "ErCu",
    "Erbium-gold": "ErAu",
    "Erbium-silver": "ErAg",
    "Erbium-Iridium": "ErIr",
    "Gadolinium(III) chloride": "GdCl3",
    "Gadolinium(III) oxide": "Gd2O3",
    "Gallium antimonide": "GaSb",
    "Gallium arsenide": "GaAs",
    "Gallium trichloride": "GaCl3",
    "Gallium nitride": "GaN",
    "Gallium phosphide": "GaP",
    "Germane": "GeH4",
    "Digermane": "Ge2H6",
    "Germanium(II) fluoride": "GeF2",
    "Germanium(IV) fluoride": "GeF4",
    "Germanium(II) chloride": "GeCl2",
    "Germanium(IV) chloride": "GeCl4",
    "Germanium(II) bromide": "GeBr2",
    "Germanium(IV) bromide": "GeBr4",
    "Germanium(II) iodide": "GeI2",
    "Germanium(IV) iodide": "GeI4",
    "Germanium(II) oxide": "GeO",
    "Germanium(IV) oxide": "GeO2",
    "Germanium(II) sulfide": "GeS",
    "Germanium(IV) sulfide": "GeS2",
    "Germanium(II) selenide": "GeSe",
    "Germanium(IV) selenide": "GeSe2",
    "Germanium telluride": "GeTe",
    "Germanium(IV) nitride": "Ge3N4",
    "Gold(I) chloride": "AuCl",
    "Gold(III) chloride": "AuCl3",
    "Gold(I,III) chloride": "Au4Cl8",
    "Gold(III) chloride": "(AuCl3)2",
    "Gold(III) fluoride": "AuF3",
    "Gold(V) fluoride": "AuF5",
    "Gold(I) bromide": "AuBr",
    "Gold(III) bromide": "(AuBr3)2",
    "Gold(I) iodide": "AuI",
    "Gold(III) iodide": "AuI3",
    "Gold(I) hydride": "AuH",
    "Gold(III) oxide": "Au2O3",
    "Gold(I) sulfide": "Au2S",
    "Gold(III) sulfide": "Au2S3",
    "Gold(III) selenide": "AuSe",
    "Gold(III) selenide": "Au2Se3",
    "Gold ditelluride": "AuTe2",
    "Hafnium tetrafluoride": "HfF4",
    "Hafnium tetrachloride": "HfCl4",
    "Hexadecacarbonylhexarhodium": "Rh6(CO)16",
    "Hydrazine": "N2H4",
    "Hydrazoic acid": "HN3",
    "Hydrobromic acid": "HBr",
    "Hydrochloric acid": "HCl",
    "Hydroiodic acid": "HI",
    "Hydrogen bromide": "HBr",
    "Hydrogen chloride": "HCl",
    "Hydrogen fluoride": "HF",
    "Hydrogen peroxide": "H2O2",
    "Hydrogen selenide": "H2Se",
    "Hydrogen sulfide": "H2S",
    "Hydrogen telluride": "H2Te",
    "Hydroxylamine": "NH2OH",
    "Hypochlorous acid": "HClO",
    "Hypophosphorous acid": "H3PO2",
    "Indium antimonide": "InSb",
    "Indium arsenide": "InAs",
    "Indium(I) chloride": "InCl",
    "Indium nitride": "InN",
    "Indium phosphide": "InP",
    "Iodic acid": "HIO3",
    "Iodine heptafluoride": "IF7",
    "Iodine pentafluoride": "IF5",
    "Iodine monochloride": "ICl",
    "Iodine trichloride": "ICl3",
    "Iridium(IV) chloride": "IrCl4",
    "Iron(II) chloride": "FeCl2",
    "Iron(III) chloride": "FeCl3",
    "Iron Ferrocyanide": "Fe7(CN)18",
    "Iron(II) oxide": "FeO",
    "Iron(III) nitrate": "Fe(NO3)3(H2O)9",
    "Iron(II,III) oxide": "Fe3O4",
    "Iron(III) oxide": "Fe2O3",
    "Iron(III) thiocyanate": "Fe(SCN)3",
    "Krypton difluoride": "KrF2",
    "Lanthanum carbonate": "La2(CO3)3",
    "Lanthanum magnesium": "LaMg",
    "Lanthanum aluminium": "LaAl",
    "Lanthanum zinc": "LaZn",
    "Lanthanum silver": "LaAg",
    "Lanthanum cadmium": "LaCd",
    "Lanthanum mercury": "LaHg",
    "Lanthanum tallium": "LaTl",
    "Lead(II) carbonate": "Pb(CO3)",
    "Lead(II) chloride": "PbCl2",
    "Lead(II) iodide": "PbI2",
    "Lead(II) nitrate": "Pb(NO3)2",
    "Lead hydrogen arsenate": "PbHAsO4",
    "Lead(II) oxide": "PbO",
    "Lead(IV) oxide": "PbO2",
    "Lead(II) phosphate": "Pb3(PO4)2",
    "Lead(II) sulfate": "Pb(SO4)",
    "Lead(II) selenide": "PbSe",
    "Lead(II) sulfide": "PbS",
    "Lead(II) telluride": "PbTe",
    "Lithium aluminium hydride": "LiAlH4",
    "Lithium bromide": "LiBr",
    "Lithium borohydride": "LiBH4",
    "Lithium carbonate (Lithium salt)": "Li2CO3",
    "Lithium chloride": "LiCl",
    "Lithium hypochlorite": "LiClO",
    "Lithium chlorate": "LiClO3",
    "Lithium perchlorate": "LiClO4",
    "Lithium cobalt oxide": "LiCoO2",
    "Lithium peroxide": "Li2O2",
    "Lithium hydride": "LiH",
    "Lithium hydroxide": "LiOH",
    "Lithium iodide": "LiI",
    "Lithium iron phosphate": "FeLiO4P",
    "Lithium nitrate": "LiNO3",
    "Lithium sulfide": "Li2S",
    "Lithium sulfite": "HLiO3S",
    "Lithium sulfate": "Li2SO4",
    "Lithium superoxide": "LiO2",
    "Magnesium antimonide": "MgSb",
    "Magnesium carbonate": "MgCO3",
    "Magnesium chloride": "MgCl2",
    "Magnesium oxide": "MgO",
    "Magnesium phosphate": "Mg3(PO4)2",
    "Magnesium sulfate": "MgSO4",
    "Manganese(IV) oxide (manganese dioxide)": "MnO2",
    "Manganese(II) sulfate monohydrate": "MnSO4.H2O",
    "Manganese(II) chloride": "MnCl2",
    "Manganese(III) chloride": "MnCl3",
    "Manganese(IV) fluoride": "MnF4",
    "Manganese(II) phosphate": "Mn3(PO4)2",
    "Mercury(I) chloride": "Hg2Cl2",
    "Mercury(II) chloride": "HgCl2",
    "Mercury fulminate": "Hg(ONC)2",
    "Mercury(II) selenide": "HgSe",
    "Mercury(I) sulfate": "Hg2SO4",
    "Mercury(II) sulfate": "HgSO4",
    "Mercury(II) sulfide": "HgS",
    "Mercury(II) telluride": "HgTe",
    "Metaphosphoric acid": "HPO3",
    "Molybdenum trioxide": "MoO3",
    "Molybdenum disulfide": "MoS2",
    "Molybdenum hexacarbonyl": "C6O6Mo",
    "Molybdic acid": "H2MoO4",
    "Neodymium(III) chloride": "NdCl3",
    "Nessler's reagent": "K2[HgI4]",
    "Nickel(II) carbonate": "NiCO3",
    "Nickel(II) hydroxide": "Ni(OH)2",
    "Nickel(II) nitrate": "Ni(NO3)2",
    "Nickel(II) oxide": "NiO",
    "Niobium oxychloride": "NbOCl3",
    "Niobium pentachloride": "NbCl5",
    "Nitric acid": "HNO3",
    "Nitrogen monoxide": "NO",
    "Nitrogen dioxide": "NO2",
    "Nitrosylsulfuric acid": "NOHSO4",
    "Osmium tetroxide (osmium(VIII) oxide)": "OsO4",
    "Osmium trioxide (osmium(VI) oxide)": "OsO3",
    "Oxybis(tributyltin)": "C24H54OSn2",
    "Oxygen difluoride": "OF2",
    "Ozone": "O3",
    "Palladium(II) chloride": "PdCl2",
    "Palladium(II) nitrate": "Pd(NO3)2",
    "Pentaborane": "B5H9",
    "Pentasulfide antimony": "Sb2S5",
    "Perchloric acid": "HClO4",
    "Perchloryl fluoride": "ClFO3",
    "Persulfuric acid (Caro's acid)": "H2SO5",
    "Perxenic acid": "H4XeO6",
    "Phenylarsine oxide": "(C6H5)AsO",
    "Phenylphosphine": "C6H7P",
    "Phosgene": "COCl2",
    "Phosphine": "PH3",
    "Phosphite": "HPO32-",
    "Phosphomolybdic acid": "H3PMo12O40",
    "Phosphoric acid": "H3PO4",
    "Phosphorous acid (Phosphoric(III) acid)": "H3PO3",
    "Phosphorus pentabromide": "PBr5",
    "Phosphorus pentafluoride": "PF5",
    "Phosphorus pentasulfide": "P4S10",
    "Phosphorus pentoxide": "P2O5",
    "Phosphorus sesquisulfide": "P4S3",
    "Phosphorus tribromide": "PBr3",
    "Phosphorus trichloride": "PCl3",
    "Phosphorus trifluoride": "PF3",
    "Phosphorus triiodide": "PI3",
    "Phosphotungstic acid": "H3PW12O40",
    "Platinum(II) chloride": "PtCl2",
    "Platinum(IV) chloride": "PtCl4",
    "Plutonium(III) chloride": "PuCl3",
    "Plutonium dioxide (Plutonium(IV) oxide)": "PuO2",
    "Potassium aluminium fluoride": "KAlF4",
    "Potassium borate": "K2B4O7•4H2O",
    "Potassium bromide": "KBr",
    "Potassium calcium chloride": "KCaCl3",
    "Potassium carbonate": "K2CO3",
    "Potassium chlorate": "KClO3",
    "Potassium chloride": "KCl",
    "Potassium cyanide": "KCN",
    "Potassium ferrioxalate": "K3[Fe(C2O4)3]",
    "Potassium hydrogencarbonate": "KHCO3",
    "Potassium hydrogen fluoride": "HF2K",
    "Potassium hydroxide": "KOH",
    "Potassium iodide": "KI",
    "Potassium iodidate": "KIO3",
    "Potassium monopersulfate": "K2SO4·KHSO4·2KHSO5",
    "Potassium nitrate": "KNO3",
    "Potassium perbromate": "KBrO4",
    "Potassium perchlorate": "KClO4",
    "Potassium permanganate": "KMnO4",
    "Potassium sulfate": "K2SO4",
    "Potassium sulfide": "K2S",
    "Potassium titanyl phosphate": "KTiOPO4",
    "Potassium vanadate": "KVO3",
    "Praseodymium(III) chloride": "PrCl3",
    "Protonated molecular hydrogen": "H3+",
    "Prussian blue (Iron(III) hexacyanoferrate(II))": "Fe4[Fe(CN)6]3",
    "Pyrosulfuric acid": "H2S2O7",
    "Radium chloride": "RaCl2",
    "Radon difluoride": "RnF2",
    "Rhodium(III) chloride": "RhCl3",
    "Rubidium bromide": "RbBr",
    "Rubidium chloride": "RbCl",
    "Rubidium fluoride": "RbF",
    "Rubidium hydroxide": "RbOH",
    "Rubidium iodide": "RbI",
    "Rubidium nitrate": "RbNO3",
    "Rubidium oxide": "Rb2O",
    "Rubidium telluride": "Rb2Te",
    "Ruthenium(VIII) oxide": "RuO4",
    "Samarium(II) iodide": "SmI2",
    "Samarium(III) chloride": "SmCl3",
    "Scandium(III) triflate": "Sc(OSO2CF3)3",
    "Scandium(III) chloride": "ScCl3",
    "Scandium(III) fluoride": "ScF3",
    "Scandium(III) nitrate": "Sc(NO3)3",
    "Scandium(III) oxide": "Sc2O3",
    "Selenic acid": "H2SeO4",
    "Selenious acid": "H2SeO3",
    "Selenium trioxide": "SeO3",
    "Selenium tetrafluoride": "SeF4",
    "Selenium hexafluoride": "SeF6",
    "Selenium hexasulfide": "Se2S6",
    "Selenium tetrachloride": "SeCl4",
    "Selenium dioxide": "SeO2",
    "Selenium disulfide": "SeS2",
    "Selenium oxydichloride": "SeOCl2",
    "Selenium oxybromide": "SeOBr2",
    "Selenoyl fluoride": "SeO2F2",
    "Samarium(III) chloride": "SmCl3",
    "Scandium(III) triflate": "Sc(OSO2CF3)3",
    "Scandium(III) chloride": "ScCl3",
    "Scandium(III) fluoride": "ScF3",
    "Scandium(III) nitrate": "Sc(NO3)3",
    "Scandium(III) oxide": "Sc2O3",
    "Silane": "SiH4",
    "Silica gel": "SiO2·nH2O",
    "Silicic acid": "[SiOx(OH)4-2x]n",
    "Silicon tetrabromide": "SiBr4",
    "Silicon carbide": "SiC",
    "Silicochloroform, Trichlorosilane": "Cl3HSi",
    "Silicofluoric acid": "H2SiF6",
    "Silicon dioxide": "SiO2",
    "Silicon tetrachloride": "SiCl4",
    "Silicon monoxide": "SiO",
    "Silicon nitride": "Si3N4",
    "Silver azide": "AgN3",
    "Silver bromate": "AgBrO3",
    "Silver bromide": "AgBr",
    "Silver chloride": "AgCl",
    "Silver chlorate": "AgClO3",
    "Silver chromate": "Ag2CrO4",
    "Silver(I) fluoride": "AgF",
    "Silver(II) fluoride": "AgF2",
    "Silver subfluoride": "Ag2F",
    "Silver fluoroborate": "AgBF4",
    "Silver fulminate": "AgCNO",
    "Silver hydroxide": "AgOH",
    "Silver iodide": "AgI",
    "Silver nitrate": "AgNO3",
    "Silver nitride": "Ag3N",
    "Silver oxide": "Ag2O",
    "Silver orthophosphate": "Ag3PO4",
    "Silver perchlorate": "AgClO4",
    "Silver sulfide": "Ag2S",
    "Silver sulfate": "Ag2SO4",
    "Sodamide": "NaNH2",
    "Sodium aluminate": "NaAlO2",
    "Sodium azide": "NaN3",
    "Sodium borohydride": "NaBH4",
    "Sodium bromide": "NaBr",
    "Sodium bromite": "NaBrO2",
    "Sodium bromate": "NaBrO3",
    "Sodium perbromate": "NaBrO4",
    "Sodium hypobromite": "NaBrO",
    "Sodium borate": "Na2B4O7",
    "Sodium perborate": "NaBO3.nH2O",
    "Sodium carbonate": "Na2CO3",
    "Sodium carbide": "Na2C2",
    "Sodium chloride": "NaCl",
    "Sodium chlorite": "NaClO2",
    "Sodium chlorate": "NaClO3",
    "Sodium perchlorate": "NaClO4",
    "Sodium cyanide": "NaCN",
    "Sodium cyanate": "NaCNO",
    "Sodium dioxide": "NaO2",
    "Sodium ferrocyanide": "Na4Fe(CN)6",
    "Sodium hydride": "NaH",
    "Sodium hydrogen carbonate (Sodium bicarbonate)": "NaHCO3",
    "Sodium hydrosulfide": "NaSH",
    "Sodium hydroxide": "NaOH",
    "Sodium hypochlorite": "NaOCl",
    "Sodium iodide": "NaI",
    "Sodium iodate": "NaIO3",
    "Sodium periodate": "NaIO4",
    "Sodium hypoiodite": "NaIO",
    "Sodium monofluorophosphate (MFP)": "Na2PFO3",
    "Sodium molybdate": "Na2MoO4",
    "Sodium manganate": "Na2MnO4",
    "Sodium nitrate": "NaNO3",
    "Sodium nitrite": "NaNO2",
    "Sodium oxide": "Na2O",
    "Sodium percarbonate": "2Na2CO3.3H2O2",
    "Sodium phosphate; see Trisodium phosphate": "Na3PO4",
    "Sodium hypophosphite": "NaPO2H2",
    "Sodium nitroprusside": "Na2[Fe(CN)5NO].2H2O",
    "Sodium persulfate": "Na2S2O8",
    "Sodium peroxide": "Na2O2",
    "Sodium perrhenate": "NaReO4",
    "Sodium permanganate": "NaMnO4",
    "Sodium persulfate": "Na2S2O8",
    "Sodium selenite": "Na2SeO3",
    "Sodium selenate": "Na2O4Se",
    "Sodium selenide": "Na2Se",
    "Sodium biselenide": "NaHSe",
    "Sodium silicate": "Na2SiO3",
    "Sodium sulfate": "Na2SO4",
    "Sodium sulfide": "Na2S",
    "Sodium sulfite": "Na2SO3",
    "Sodium tellurite": "Na2TeO3",
    "Sodium tungstate": "Na2WO4",
    "Sodium thioantimoniate": "Na3(SbS4).9H2O",
    "Sodium thiocyanate": "NaSCN",
    "Sodium thiocyanate": "Na2S2O3",
    "Sodium uranate": "Na2O7U2",
    "Stannous chloride (tin(II) chloride)": "SnCl2",
    "Stibine": "SbH3",
    "Strontium carbonate": "SrCO3",
    "Strontium chloride": "SrCl2",
    "Strontium hydroxide": "Sr(OH)2",
    "Strontium nitrate": "Sr(NO3)2",
    "Strontium oxide": "SrO",
    "Strontium titanate": "SrTiO3",
    "Sulfamic acid": "H3NO3S",
    "Sulfane": "H2S",
    "Sulfur dioxide": "SO2",
    "Sulfur tetrafluoride": "SF4",
    "Sulfur hexafluoride": "SF6",
    "Disulfur decafluoride": "S2F10",
    "Sulfuric acid": "H2SO4",
    "Sulfurous acid": "H2SO3",
    "Sulfuryl chloride": "SO2Cl2",
    "Tantalum carbide": "TaC",
    "Tantalum(V) oxide": "Ta2O5",
    "Telluric acid": "H6TeO6",
    "Tellurium dioxide": "TeO2",
    "Tellurium tetrachloride": "TeCl4",
    "Tellurous acid": "H2TeO3",
    "Terbium(III) chloride": "TbCl3",
    "Tetraborane(10)": "B4H10",
    "Tetrachloroauric acid": "AuCl3",
    "Tetrafluorohydrazine": "N2F4",
    "Tetramminecopper(II) sulfate": "[Cu(NH3)4]SO4",
    "Tetrasulfur tetranitride": "S4N4",
    "Thallium(I) carbonate": "Tl2CO3",
    "Thallium(I) fluoride": "TlF",
    "Thallium(III) oxide": "Tl2O3",
    "Thallium(III) sulfate": "Tl2(SO4)2",
    "Thionyl chloride": "SOCl2",
    "Thiophosgene": "CSCl2",
    "Thiophosphoryl chloride": "Cl3PS",
    "Thorium dioxide": "ThO2",
    "Thortveitite": "(Sc,Y)2Si2O7",
    "Thulium(III) chloride": "TmCl3",
    "Tin(II) chloride": "SnCl2",
    "Tin(II) fluoride": "SnF2",
    "Tin(IV) chloride": "SnCl4",
    "Titanium boride": "TiB2",
    "Titanium carbide": "TiC",
    "Titanium dioxide (titanium(IV) oxide)": "TiO2",
    "Titanium dioxide (B) (titanium(IV) oxide)": "TiO2",
    "Titanium nitride": "TiN",
    "Titanium(IV) bromide (titanium tetrabromide)": "TiBr4",
    "Titanium(IV) chloride (titanium tetrachloride)": "TiCl4",
    "Titanium(III) chloride": "TiCl3",
    "Titanium(II) chloride": "TiCl2",
    "Titanium(IV) iodide (titanium tetraiodide)": "TiI4",
    "Trifluoromethylisocyanide": "C2NF3",
    "Trifluoromethanesulfonic acid": "CF3SO3H",
    "Trimethylphosphine": "C3H9P",
    "Trioxidane": "H2O3",
    "Tripotassium phosphate": "K3PO4",
    "Trisodium phosphate": "Na3PO4",
    "Triuranium octaoxide (pitchblende or yellowcake)": "U3O8",
    "Tungsten carbide": "WC",
    "Tungsten(VI) chloride": "WCl6",
    "Tungsten(VI) Fluoride": "WF6",
    "Tungstic acid": "H2WO4",
    "Tungsten hexacarbonyl": "W(CO)6",
    "Uranium hexafluoride": "UF6",
    "Uranium pentafluoride": "UF5",
    "Uranium tetrachloride": "UCl4",
    "Uranium tetrafluoride": "UF4",
    "Uranyl carbonate": "UO2CO3",
    "Uranyl chloride": "UO2Cl2",
    "Uranyl fluoride": "UO2F2",
    "Uranyl hydroxide": "UO2(OH)2",
    "Uranyl hydroxide": "(UO2)2(OH)4",
    "Uranyl nitrate": "UO2(NO3)2",
    "Uranyl sulfate": "UO2SO4",
    "Vanadium carbide": "VC",
    "Vanadium oxytrichloride (Vanadium(V) oxide trichloride)": "VOCl3",
    "Vanadium(IV) chloride": "VCl4",
    "Vanadium(II) chloride": "VCl2",
    "Vanadium(II) oxide": "VO",
    "Vanadium(III) nitride": "VN",
    "Vanadium(III) bromide": "VBr3",
    "Vanadium(III) chloride": "VCl3",
    "Vanadium(III) fluoride": "VF3",
    "Vanadium(IV) fluoride": "VF4",
    "Vanadium(III) oxide": "V2O3",
    "Vanadium(IV) oxide": "VO2",
    "Vanadium(IV) sulfate": "VOSO4",
    "Vanadium(V) oxide": "V2O5",
    "Water": "H2O",
    "Xenon difluoride": "XeF2",
    "Xenon hexafluoroplatinate": "Xe[PtF6]",
    "Xenon tetrafluoride": "XeF4",
    "Xenon tetroxide": "XeO4",
    "Xenic acid": "H2XeO4",
    "Ytterbium(III) chloride": "YbCl3",
    "Ytterbium(III) oxide": "Yb2O3",
    "Yttrium(III) antimonide": "YSb",
    "Yttrium(III) arsenide": "YAs",
    "Yttrium(III) bromide": "YBr3",
    "Yttrium aluminium garnet": "Y3Al5O12",
    "Yttrium barium copper oxide": "YBa2Cu3O7",
    "Yttrium(III) fluoride": "YF3",
    "Yttrium iron garnet": "Y3Fe5O12",
    "Yttrium(III) oxide": "Y2O3",
    "Yttrium(III) sulfide": "Y2S3",
    "Yttrium copper": "YCu",
    "Yttrium silver": "YAg",
    "Yttrium gold": "YAu",
    "Yttrium rhodium": "YRh",
    "Yttrium iridium": "YIr",
    "Yttrium zinc": "YZn",
    "Yttrium cadmium": "YCd",
    "Yttrium magnesium": "YMg",
    "Zinc bromide": "ZnBr2",
    "Zinc carbonate": "ZnCO3",
    "Zinc chloride": "ZnCl2",
    "Zinc cyanide": "Zn(CN)2",
    "Zinc fluoride": "ZnF2",
    "Zinc iodide": "ZnI2",
    "Zinc oxide": "ZnO",
    "Zinc selenide": "ZnSe",
    "Zinc sulfate": "ZnSO4",
    "Zinc sulfide": "ZnS",
    "Zinc telluride": "ZnTe",
    "Zirconia hydrate": "ZrO2·nH2O",
    "Zirconium carbide": "ZrC",
    "Zirconium(IV) chloride": "ZrCl4",
    "Zirconium nitride": "ZrN",
    "Zirconium hydroxide": "Zr(OH)4",
    "Zirconium(IV) oxide": "ZrO2",
    "Zirconium orthosilicate": "ZrSiO4",
    "Zirconium tetrahydroxide": "H4O4Zr",
    "Zirconium tungstate": "ZrW2O8", # from here user suggested
    "Azidoazide azide": "C2N14",
    "Tungsten dioxide": "OWO",
    "Uranium pentabromide": "UBr5",
    "6,9,12,15,18,29,32,35,38,41,52,55,58,61,64-\
    pentadecaoxaheptacyclo\
    [63.4.0.05,69.019,24.023,28.042,47.046,51]\
    nonahexaconta-1(69),2,4,19,21,23,25,27,42,44,46,48,50,65,67-\
    pentadecaene;5,12,19,26-tetrazoniaheptacyclo\
    [24.2.2.22,5.27,10.212,15.216,19.221,24]\
    tetraconta-1(29),2(40),3,5(39),7,9,12,14,16(34),17,19(33),21(32),22,24(31),26(30),27,35,37-\
    octadecaene;dodecahexafluorophosphate": "C228H236F72N12O30P12",
    "Barrium ferrate": "BaFeO4",
    "Potassium ferrate": "K2FeO4",
    "Arsenic sulfide": "AsS",
    "Buckminsterfullerene": "C60",
    "Cubane": "C8H8" } 


numbers_discord =	{
    "0️⃣": 0,
    "1️⃣": 1,
    "2️⃣": 2,
    "3️⃣": 3,
    "4️⃣": 4,
    "5️⃣": 5,
    "6️⃣": 6,
    "7️⃣": 7,
    "8️⃣": 8,
    "9️⃣": 9,
    "🇦": 10,
    "🇧": 11,
    "🇨": 12,
    "🇩": 13,
    "🇪": 14,
    "🇫": 15
}

discord_numbers =	{
    0: "0️⃣",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🇦",
    11: "🇧",
    12: "🇨",
    13: "🇩",
    14: "🇪",
    15: "🇫"
}

class minigame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("loaded minigame")

        # ! run the task
        self.check_expired_roles.start()


##### -------- TASKS  -------- TASKS -------- TASKS  -------- #####

    # ! every 1h check and remove roles, also msg the user nad let him know if you can't
    @tasks.loop(minutes=30) # 3600s = every hour
    async def check_expired_roles(self):
        # gets run on start and every xyz
        current_roles = await list_all_active_roles_db()
        for role in current_roles:
            date = datetime.datetime.strptime(str(role[3]), time_format)
            if date < datetime.datetime.today():
                # ! remove role, and delete entry
                # remove role
                try:
                    guild = await self.bot.fetch_guild(role[0])
                    user_role = discord.utils.find(lambda m: m.id == role[2], guild.roles)
                    user = await guild.fetch_member(role[1])
                except Exception as err:
                    print(err)
                    await delete_user_role_from_db(role[0], role[1], role[2])
                    return
                try:
                    await user.remove_roles(user_role)
                    await delete_user_role_from_db(role[0], role[1], role[2])
                except Exception as err:
                    await user.send(f"hey, I can't remove the role ({user_role.name}) that exprired from you \
                        \n It's your duty now to ask an admin on {guild.name} to remove that from you")
                print(f"role removed ! {user_role.name}")
            else:
                pass

    # ! when COG unloads, cancel all tasks!
    def cog_unload(self):
        self.check_expired_roles.cancel()

    # ! check if has internet, pause as long as no internet
    @check_expired_roles.before_loop
    async def before_check_expired_roles(self):
        await self.bot.wait_until_ready()

##### -------- TASKS  -------- TASKS -------- TASKS  -------- #####




#! ----------------------------------------- TESTING -----------------------------------------

    @commands.Cog.listener()
    async def on_ready(self):
        pass
        # do nothing, no need
    

    @commands.check(dev_check)
    @commands.command()
    async def minitest2(self, ctx):
        pass
        # taskz = check_expired_roles.get_task()
        # taskz.cancel()
        # taskz = asyncio.get_event_loop()
        # print(taskz)
        # taskz.stop()
        try:
            await create_table_minigame_settings(local_db)
            await create_table_role_settings(local_db)
            await ctx.send("table added")
        except Exception as err:
            await ctx.send(err)

#! ----------------------------------------- TESTING -----------------------------------------

# TODO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> developer only <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # ! sets points to user id, DEV only !
    @commands.check(dev_check)
    @commands.command()
    async def setpoints(self, ctx, discord_id, points):
        await addpoints(discord_id, points)
        await ctx.send("set")

    # ! removes user from the database, for any reasons
    @commands.check(dev_check)
    @commands.command()
    async def removeuser(self, ctx, discord_id):
        await deleteplayer(discord_id)
        await ctx.send("removed")

# TODO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> developer only <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# ? ADMIN COMMANDS

    # add server to the feature/poo
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def togglerolepurchasing(self, ctx):
        #check, flip
        is_opted = await optin_check(ctx.guild.id)
        if is_opted: # will opt out
            message = await ctx.send("You are about to disable the ability of buying roles with coins from minigame, are you sure?\
            if so, please type **YES**")
        else: # will opt in
            message = await ctx.send("bunch of bullshit explaining how this shit works, someone help me?\
            enable buying roles, please type **YES**")

        def pred(m):
            if m.author.id == ctx.author.id:
                return True
            else:
                return False
        try:
            msg = await self.bot.wait_for('message', check=pred, timeout=300.0)
            #print(msg.channel.id)
        except asyncio.TimeoutError:
            await message.edit(content='Timed out ?')
            return
        else:
            if msg.content.lower() == "yes":
                await optin_change(ctx.guild.id, not (await optin_check(ctx.guild.id)))
                if await optin_check(ctx.guild.id):
                    await message.edit(content=f'sussesfully enabled !')
                else:
                    await message.edit(content=f'sussesfully disabled !')

            else:
                await message.edit(content=f'cancelled !')




# ? USER COMMANDS

    # ! check is server is enabled
    @commands.command()
    async def rolepurchasepermitted(self, ctx):
        if await optin_check(ctx.guild.id):
            await ctx.send("You can buy roles on this server")
        else:
            await ctx.send("Server is lame, you can't buy roles here, ask admin to run .togglerolepurchasing")

    # ! shop, you can buy roles
    @commands.command()
    async def shop(self, ctx, role_name):

        # TODO rewrite this help crap
        if role_name.lower() == "help":

            embed = discord.Embed(
                title=f"{self.bot.user.name} shop info (THIS BOT IS IN BETA!)",
                colour=discord.Colour(0x3b12ef),
                # url="https://discordapp.com/",
                # description="help",
            )
            # embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/1.png") # TODO later
            embed.set_author(
                name=f"{self.bot.user.name}",
                url="https://tcw-sciencebot.discord-bot.thechemicalworkshop.com", 
                icon_url=f"{self.bot.user.avatar_url}"
            )
            embed.set_footer(
                text=f"{self.bot.thanks()}",
                icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
            )
            # -------------------

            colors_string = ""
            for roles in minigame_shop_roles:
                role = discord.utils.find(lambda m: m.name.lower() == roles.lower(), ctx.guild.roles)
                if role:
                    colors_string += f"{role.mention}\n"


            embed.add_field(
                name=f"You can buy a color, available colors",
                value=colors_string,
                inline=False
            )


            await ctx.send(embed=embed)
            return

        if not await optin_check(ctx.guild.id):
            await ctx.send("Unfortunatly, admins of this server didn't allow the shop to run !")
            return

        if role_name.lower() not in minigame_shop_roles:
            await ctx.send(f"Unfortunatly this role does not exist, type {ctx.prefix}shop help for available roles")
            return

        role_cost = 100 # ! FIX ME ...............................
        role_duration = 24*7 # in hours # ! FIX ME ...............................

        my_points = await mypoints(ctx.author.id)
        if my_points < role_cost:
            await ctx.send(f"Sorry, you cannot afford the role :( you need {role_cost} points")
            return

        # * reactivechem yellow easter egg
        if role_name.lower() == "yellow" and ctx.guild.id == 644966555930853390:
            await addpoints(ctx.author.id, my_points-role_cost)
            message = await ctx.send("Enjoy your new role in 3...")
            await asyncio.sleep(1)
            await message.edit(content="Enjoy your new role in 2...")
            await asyncio.sleep(1)
            await message.edit(content="Enjoy your new role in 1...")
            await asyncio.sleep(1)
            await message.edit(content="<:yellowchem:717858591335514112>")
            await asyncio.sleep(3)
            await ctx.guild.kick(ctx.author, reason="yellow chem bad")
            await message.edit(content="lmao he got banned for yellow chem")
            return
        # * reactivechem yellow easter egg


        message = await ctx.send("Checking...")
        await asyncio.sleep(5)

        role = discord.utils.find(lambda m: m.name.lower() == role_name.lower(), ctx.guild.roles)
        if not role:
            await message.edit(content=f"admin of this server needs to create the role **{role_name.lower()}** so i can give it to you")
            return
        try:
            await ctx.author.add_roles(role)
        except Exception as err:
            await message.edit(content=err)
            await print(err)
            await print(ctx.guild.id)
            return
        # print("good so far")
        await addpoints(ctx.author.id, my_points-role_cost)

        # add expiration
        try:
            current_date = datetime.datetime.today()
            expiration_date = (current_date + datetime.timedelta(hours=role_duration)).strftime(time_format)
            # expiration_date = (current_date + datetime.timedelta(minutes=1)).strftime(time_format)
            await add_user_role_to_db(ctx.guild.id, ctx.author.id, role.id, expiration_date)
            await message.edit(content=f"your role expires on {expiration_date} (UTC)")
        except Exception as err:
            print(err)
            print(ctx.author.id)
            print(ctx.guild.id)
            print(role.id)
        # # await ctx.send(end_date.strftime("%Y%m%d"))

        # print(f"ADDED ROLE ! {ctx.author.id} {role.id}")
        # await asyncio.sleep(role_duration*60*60*24) # wait role_duartion days
        # await ctx.author.remove_roles(role)
        # print(f"REMOVED ROLE ! {ctx.author.id} {role.id}")
        # await ctx.author.send(f"hey, just letting your know, that your role **{role.name}** exipred")

    # ! transfer money
    @commands.command()
    async def transfer(self, ctx, user: discord.Member, ammount_unfiltered):

        jakub_user = self.bot.get_user(700542051451928638) #! jakub id

        if ammount_unfiltered.isdigit() == False:
            await ctx.send(f"ammount must be a number !")
            return
        else:
            ammount = int(ammount_unfiltered)

        if not ammount >= 100:
            await ctx.send("you must send at least 100 points")
            return
        if not ammount % 10 == 0:
            await ctx.send("Must be divisible by 10 !")
            return



        if user.bot:
            await ctx.send(f"Sorry, {jakub_user} already tried abusing this\nDONT\'T SEND MONEY TO BOTS")
            return

        if ctx.author.id == int(user.id):
            await ctx.send(f"Sorry, {jakub_user} already tried abusing this\nDONT\'T SEND MONEY TO YOURSELF")
            return

        my_points = await mypoints(ctx.author.id)

        if not my_points >= ammount:
            await ctx.send("you can't give someone more money then you have")
            return
        try:
            user = await self.bot.fetch_user(user.id)
        except discord.errors.NotFound:
            await ctx.send("user not found")
            return

        premium = False    

        for donator in self.bot.donators:
            if ctx.author.id == donator.get("discord_id"):
                premium = True 
        
        if premium:
            tax = 15
            buy_premium = ""
        else:
            tax = 20
            buy_premium ="\n TCW donators pay 15% tax instead of 20% !"

        his_points = await mypoints(user.id)
        
        tax_points = int(ammount/100*tax)

        his_new_points = int(his_points + ammount - tax_points)

        my_new_points = my_points - ammount

        print(his_new_points)

        message = await ctx.send(f"You are about to send {ammount} points to {user}\n \
            Your new balance = {my_new_points}\n \
            {user}\'s new balance = {his_new_points} \n \
            {tax}% tax = {tax_points} points{buy_premium}\n\n\
            Type **YES** to send points")

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
                pass
                await addpoints(ctx.author.id, my_new_points) # sender points
                await addpoints(user.id, his_new_points)  # receiver points
                await message.edit(content="Thank you for using TCW services, transfer compleate")
            elif msg.content.lower() == "no":
                await message.edit(content="cancelled !")
                pass
            elif msg.content.lower() == "gay":
                await message.edit(content="ok, removed 100 points from your account for beeing rude")
                await addpoints(ctx.author.id, my_points-100)    
                pass
            elif msg.content.lower() == "yellow chem":
                await message.edit(content="ok, removed 50 points from your account for beeing rude")
                await addpoints(ctx.author.id, my_points-50)    
                pass
            else:
                await message.edit(content="...?")
                return

    # ! mercy, if you have less than -1000 points
    @commands.command()
    async def mercy(self, ctx):
        my_points = await mypoints(ctx.author.id)

        if my_points >= 100:
            await ctx.send("Who's greedy, looses")
            await addpoints(ctx.author.id, my_points-10)
            return

        if not my_points <= 0:
            await ctx.send(f"You have {my_points}, 0 or less")
            return
        else:
            await ctx.send(f"{my_points} points? how did you fuck up so badly...?\n\
            resetting your points to 0 !")
            await addpoints(ctx.author.id, 0)

    # ! shows your coins/score
    @commands.command(aliases = ["coins"])
    async def points(self, ctx, *, user: discord.Member = None):
        
        if user != None:
            #! user was selected
            user_id = user.id
        else:
            #! default user 
            user_id = ctx.author.id

        try:
            points = await mypoints(user_id)
        except Exception as err:
            print(err)
            await ctx.send("error? shouldn't happen lol")
            return

        good_boy = "<:this:668532855449845800>"
        very_good_boy = "💎"

        shitty_boy = "<:no:713519294071308318>"
        very_shitty_boy = "💩"
        
        if points > 99:
            my_number = int(points / 100)
            my_rating = very_good_boy* int(my_number) #! just for reactive chem server
        elif points > 19:
            my_number = int(points / 20)
            my_rating = good_boy* int(my_number) #! just for reactive chem server
        elif points == 0:
            my_rating = "" #! just for reactive chem server
        elif points < -99:
            my_number = int(abs(points) / 100)
            my_rating = very_shitty_boy* int(my_number) #! just for reactive chem server
        elif points < -19:
            my_number = int(abs(points) / 20)
            my_rating = shitty_boy* int(my_number) #! just for reactive chem server
        else:
            my_rating = "<:wierdchamp:713522961654611969>" #! just for reactive chem server

        # print(int(my_number))
        await ctx.send(f"points :{my_rating} {points} !")

    # ! shows the leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        epoints = await allpoints()
        def myFunc(e):
            return e[1]

        epoints.sort(reverse=True, key=myFunc)
        end_str = ""
        message = await ctx.send("grabbing users...")
        i = 0
        for user in epoints:
            usr = await self.bot.fetch_user(user[0])
            end_str += f"{usr.name} -> {user[1]} Points !\n"
            i+=1
            if i == 10:
                break
        await message.edit(content=end_str)

    # ! plays mninigame non coins
    @commands.command()
    async def minigame(self, ctx, diff="normal"):

        if diff == "baby":
            sleeptime = 1
            possibilities = 2
            reaction_time = 6
        elif diff == "easy":
            sleeptime = 1
            possibilities = 3
            reaction_time = 5
        elif diff == "normal":
            sleeptime = 0.7
            possibilities = 5
            reaction_time = 3
        elif diff == "hard":
            sleeptime = 0.5
            possibilities = 8
            reaction_time = 2
        elif diff == "hardcore":
            sleeptime = 0.3
            possibilities = 15
            reaction_time = 2.5
        elif diff == "quickfuck":
            sleeptime = 0.3
            possibilities = 4
            reaction_time = 1.5
        elif diff == "help":
            await ctx.send("help me write this help command\nonly normal, hard hardcore count to rank/leaderboard")
            return
        else:
            await ctx.send("available difficulties: baby, easy, **normal**, hard, hardcore, quickfuck, help")
            return

        message = await ctx.send("Loading elements...")
        nb = 1
        while nb <= possibilities:
            await message.add_reaction(discord_numbers.get(nb))
            nb += 1

        if random.randint(0,100) < 1:
            await message.edit(content=f"You suck {ctx.author.mention} no need to try")
            return

        cmp = []
        j = 1
        while j < possibilities + 1:
            # print(j)
            res = key, val = random.choice(list(compounds.items()))
            cmp.append(res)
            del compounds[key]
            j += 1

        # print("")
        cmp_copy = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}] # ? 25
        # print(type(cmp[3]))
        string = ""
        king = ""
        i = (possibilities-1)
        counter = 1
        while i >= 0:
            # print(i)
            number = random.randint(0,i)
            # print(f"rnumber = {number}")
            if random.randint(0,100) < (100/(possibilities-1)):
                king = cmp[number]
            if i == 0 and king == "":
                king = cmp[number]
            string += f"{discord_numbers.get(counter)} {cmp[number][1]}\n"
            cmp_copy[counter] = cmp[number]
            del cmp[number]
            i -= 1
            counter += 1
        string = f'{king[0]}\n\n{string}'
        e = 3
        while e >> 0:
            # print(e)
            await message.edit(content=f"{e}...")
            await asyncio.sleep(sleeptime)
            e -= 1
        await message.edit(content="Go !!!")

    
        await asyncio.sleep(1)
        await message.edit(content=string)
        # await ctx.send(king[0])
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=reaction_time, check=check)
        except asyncio.TimeoutError:

            await message.add_reaction("❌")
            await message.edit(content="Too slow !")
        else:
            if cmp_copy[numbers_discord.get(reaction.emoji)] == king:
                await message.edit(content="You won !")
            else:
                await message.edit(content=f"You lost, the correct anwser is : {king[1]}")
                # print(cmp_copy[numbers_discord.get(reaction.emoji)])
                # print(reaction.emoji)
                # print("")

    # ! plays ranked, with coins
    @commands.command()
    async def ranked(self, ctx, diff="normal"):


        sleeptime = 0.5 # 0.5
        possibilities = 7 # 7
        reaction_time = 2.5 # 2.5

        points = 0

        try:
            current_points = await mypoints(ctx.author.id)
        except Exception as err:
            print(err)
            print(f"ERROR {ctx.author.id} {points} ctx.guild.id ")
            await ctx.send(f"SOMETHING WENT HORRIBLY WRONG !")
            return

        message = await ctx.send(f"this is a ranked match ! your current points: {current_points}\ndo .coins to see your points !\nGame of HELL incomming !")
        await asyncio.sleep(sleeptime*2)


        async def match(self, ctx, message):


            nb = 1
            while nb <= possibilities:
                await message.add_reaction(discord_numbers.get(nb))
                nb += 1
            cmp = []
            j = 1
            while j < possibilities + 1:
                # print(j)
                res = key, val = random.choice(list(compounds.items()))
                cmp.append(res)
                del compounds[key]
                j += 1

            # print("")
            cmp_copy = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}] # ? 25
            # print(type(cmp[3]))
            string = ""
            king = ""
            i = (possibilities-1)
            counter = 1
            while i >= 0:
                # print(i)
                number = random.randint(0,i)
                # print(f"rnumber = {number}")
                if random.randint(0,100) < (100/(possibilities-1)):
                    king = cmp[number]
                if i == 0 and king == "":
                    king = cmp[number]
                string += f"{discord_numbers.get(counter)} {cmp[number][1]}\n"
                cmp_copy[counter] = cmp[number]
                del cmp[number]
                i -= 1
                counter += 1
            string = f'{king[0]}\n\n{string}'


            e = 3
            while e >> 0:
                await message.edit(content=f"{e}...")
                await asyncio.sleep(sleeptime)
                e -= 1
            await message.edit(content="Go !!!")
            await asyncio.sleep(1) #TODO lag optimization?
            await message.edit(content=string)
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=reaction_time, check=check)
            except asyncio.TimeoutError:
                return -5
            else:
                if cmp_copy[numbers_discord.get(reaction.emoji)] == king:
                    return 10
                else:
                    return -10

        if diff.lower() == "hard":
            rounds = 10
            bonus = 2
            await message.edit(content=f"THIS IS HARD MODE: THERE WILL BE {rounds} ROUNDS\nhowever many points you'll get will be multiplied by 2 (yes also negative)")
            await asyncio.sleep(3)
        elif diff.lower() == "normal":
            rounds = 5
            bonus = 1
        elif diff.lower() == "easy":
            rounds = 3
            bonus = 0.5
            sleeptime = 0.5 # 0.5
            possibilities = 7 # 7
            reaction_time = 3.5 # 3.5
            await message.edit(content=f"go enjoy yellow chem {rounds} rounds")
            await asyncio.sleep(3)
        elif diff.lower() == "quickfuck":
            rounds = 3
            bonus = 3
            sleeptime = 0.5 # 0.5
            possibilities = 5 # 5
            reaction_time = 1.5 # 1.5
            await message.edit(content=f"{rounds} rounds of quick {reaction_time}s enjoyment")
            await asyncio.sleep(3)
        else:
            await ctx.send(f"wrong difficulty ! type .help for help")


        while rounds >> 0:
            points += await match(self, ctx, message)
            await message.edit(content="please remove your reaction")
            await asyncio.sleep(3)
            rounds -= 1
        


        # print(points)
        # if points < 0:
        #     await ctx.guild.kick(ctx.author, reason="gay")
        # else:
        #     role = discord.utils.find(lambda m: m.id == 660907847479197718, ctx.guild.roles)
        #     await ctx.author.add_roles(role)
        # await asyncio.sleep(1)



        points = int(points*bonus) # extra plus minus points



        try:
            current_points = await mypoints(ctx.author.id)
            new_points = int(points) + int(current_points)
            await addpoints(ctx.author.id, int(new_points))
            await message.edit(content=f"Your points {points} were added to the ranking !\ndo .coins to see how much you suck")
        except Exception as err:
            print(err)
            print(f"ERROR {ctx.author.id} {points} ctx.guild.id ")
            await message.edit(content=f"ERROR YOUR POINTS DIDN'T GET ADDED FOR SOME REASON")
            return


        # print("end")






# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------

def setup(bot):
    bot.add_cog(minigame(bot))
