import json

async def get_prefix(bot, message):
    with open("settings_files/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefix = prefixes.get(str(message.guild.id))
    if not prefix:
        return "." #* default prefix
    else:
        return prefix