import json

async def get_beta_optin(message):
    with open("settings_files/beta_optin.json", "r") as f:
        optin_data = json.load(f)

    optin = optin_data.get(str(message.guild.id))
    if not optin:
        return False #* default optin
    else:
        return optin