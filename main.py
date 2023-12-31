import json
import os
import platform

import aiohttp
import disnake
from disnake.ext import commands

from utils.opener import *
from utils.var import *

if not os.path.exists(data_folder):
    os.makedirs(data_folder)
if not os.path.exists(data_file):
    with open(data_file, 'w') as data_file:
        json.dump({}, data_file)

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        token = input("Enter the bot's token:\n")
        prefix = input("Enter the bot's prefix:\n")
        api_url = input("Enter the Pterodactyl API URL:\n")
        api_key = input("Enter the Pterodactyl API key:\n")
        config_data = {
            "TOKEN": token,
            "PREFIX": prefix,
            "PTERODACTYL_API_URL": api_url,
            "PTERODACTYL_API_KEY": api_key
        }
        json.dump(config_data, config_file, indent=4)
    config = get_config()
else:
    config = get_config()

token = config["TOKEN"]
prefix = config["PREFIX"]

bot = commands.Bot(command_prefix=prefix, intents=disnake.Intents.all(), case_insensitive=True)
bot.remove_command('help')

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        nbot = bot.user.name
    else:
        nbot = bot.user.name + "#" + bot.user.discriminator

    async with aiohttp.ClientSession() as session:
        async with session.get(online_version) as response:
            if response.status == 200:
                bot_repo_version = await response.text()
            else:
                bot_repo_version = "Unknown"

    bot_version = get_bot_repo_version()

    if bot_version != bot_repo_version:
        print()
        print('===============================================')
        print('🛑 You are not using the latest version!')
        print('🛑 Please update the bot.')
        print('🛑 Use "git fetch && git pull" to update your bot.')
    print('===============================================')
    print(f"🔱 The bot is ready!")
    print(f'🔱 Logged in as {nbot} | {bot.user.id}')
    print(f'🔱 Bot local version: {bot_version}')
    print(f'🔱 Bot online version: {bot_repo_version}')
    print(f"🔱 Disnake version: {disnake.__version__}")
    print(f"🔱 Running on {platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Python version: {platform.python_version()}")
    print('===============================================')

for filename in os.listdir(cog_folder):
    if filename.endswith('.py'):
        cog_name = filename[:-3]
        try:
            bot.load_extension(f'{cog_import}{cog_name}')
        except Exception as e:
            print(f"🌪️  Error during '{cog_name}' loading:\n\n{e}")

bot.run(token)