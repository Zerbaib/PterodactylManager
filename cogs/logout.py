import json

import disnake
from disnake.ext import commands


class Logout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = 'data/'
        self.data_file = f'{self.data_folder}users.json'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /logout has been loaded')
        print()
    
    def get_data(self):
        with open(self.data_file, 'r') as data_file:
            data = json.load(data_file)
        return data

    def save_data(self, data):
        with open(self.data_file, 'w') as data_file:
            json.dump(data, data_file, indent=4)

    @commands.slash_command(name='logout', description='Logout of your Pterodactyl account')
    async def logout(self, ctx):
        data = self.get_data()
        user_id = str(ctx.author.id)
        if user_id in data:
            data.pop(user_id)
            self.save_data(data)
            await ctx.send(f'✅ You have been logged out {ctx.author.mention}!', ephemeral=True)
        else:
            await ctx.send("You are not logged in.", ephemeral=True)

def setup(bot):
    bot.add_cog(Logout(bot))