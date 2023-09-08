import json

import disnake
from disnake.ext import commands
from pydactyl import PterodactylClient


class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = 'data/'
        self.data_file = f'{self.data_folder}users.json'
        self.config_file = 'config.json'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /login has been loaded')
        print()

    def get_data(self):
        with open(self.data_file, 'r') as data_file:
            data = json.load(data_file)
        return data

    def save_data(self, data):
        with open(self.data_file, 'w') as data_file:
            json.dump(data, data_file, indent=4)

    def get_config(self):
        with open(self.config_file, 'r') as config_file:
            config = json.load(config_file)
        return config

    @commands.slash_command(name='login', description='Login to your Pterodactyl account')
    async def login(self, ctx):
        data = self.get_data()
        user_id = ctx.author.id

        if str(user_id) in data:
            return await ctx.send("You are already logged in.", ephemeral=True)

        user = ctx.author
        discord_pseudo = user.name
        discord_displayname = user.display_name
        discord_mail = f"{discord_pseudo}@server.discord"

        config = self.get_config()
        PTERODACTYL_API_URL = config.get("PTERODACTYL_API_URL")
        PTERODACTYL_API_KEY = config.get("PTERODACTYL_API_KEY")

        pterodactyl = PterodactylClient(PTERODACTYL_API_URL, PTERODACTYL_API_KEY)
        try:
            pterodactyl.create_user(discord_pseudo, discord_displayname, discord_pseudo, discord_mail)
        except Exception as e:
            return await ctx.send(f"Failed to create a Pterodactyl user:\n{str(e)}", ephemeral=True)

        api_key = pterodactyl.create_api_key(user_id)

        data[user_id] = api_key
        self.save_data(data)

        await ctx.send(f'✅ You have been logged in, {user.mention}!', ephemeral=True)

def setup(bot):
    bot.add_cog(Login(bot))
