import json
import disnake
from disnake.ext import commands


class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = 'data'
        self.data_file = f'{self.data_folder}users.json'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /server has been loaded')
        print()
    
    def get_data(self):
        with open(self.data_file, 'r') as data_file:
            data = json.load(data_file)
        return data

    def save_data(self, data):
        with open(self.data_file, 'w') as data_file:
            json.dump(data, data_file, indent=4)

    @commands.slash_command(name='server', description='View your Pterodactyl server')
    async def server(self, ctx, server=None):
        return await ctx.send(f'🚧 This command is still under construction {ctx.author.mention}!', ephemeral=True)

def setup(bot):
    bot.add_cog(Login(bot))