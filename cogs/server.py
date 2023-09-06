import json
import disnake
import requests
from disnake.ext import commands
from disnake.ui import View, button


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = 'data/'
        self.data_file = f'{self.data_folder}users.json'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /server has been loaded')
        print()
    
    def get_config(self):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config

    def get_data(self):
        with open(self.data_file, 'r') as data_file:
            data = json.load(data_file)
        return data

    def save_data(self, data):
        with open(self.data_file, 'w') as data_file:
            json.dump(data, data_file, indent=4)

    @commands.slash_command(name='server', description='View your Pterodactyl server')
    async def server(self, ctx, server=None):
        user_id = ctx.author.id
        data = self.get_data()
        config = self.get_config()

        PTERODACTYL_API_URL = config["PTERODACTYL_API_URL"]

        if str(user_id) not in data:
            return await ctx.send("# 🛑 You are not logged.\n## ⚠️ Please do ``/login <your_api_key>``\n### For get your api key please pm an admin", ephemeral=True)
        
        api_key = data[str(user_id)]

        try:
            if server is None:
                response = requests.get(f"{PTERODACTYL_API_URL}/user/{user_id}/servers",
                                        headers={"Authorization": f"Bearer {api_key}"})
                response.raise_for_status()
                servers = response.json()
                server_list = "\n".join([f"{server['name']} ({server['id']})" for server in servers])
                await ctx.send(f"Here is the list of your servers:\n```{server_list}```")
            else:
                response = requests.get(f"{PTERODACTYL_API_URL}/user/{user_id}/server/{server}",
                                        headers={"Authorization": f"Bearer {api_key}"})
                response.raise_for_status()
                server_info = response.json()
                embed = disnake.Embed(title=f"Server: {server_info['name']}")
                
                cpu_used = server_info['cpu']
                cpu_max = server_info['cpu_max']
                embed.add_field(name="CPU Usage", value=f"{cpu_used} / {cpu_max}", inline=True)

                ram_used = server_info['ram']
                ram_max = server_info['ram_max']
                embed.add_field(name="RAM Usage", value=f"{ram_used} / {ram_max}", inline=True)

                storage_used = server_info['storage']
                storage_max = server_info['storage_max']
                embed.add_field(name="Storage", value=f"{storage_used}MB / {storage_max}MB", inline=True)

                view = View()
                view.add_item(button.Button(style=disnake.ButtonStyle.primary, label="Start", custom_id=f"start_server_{server_info['id']}"))
                view.add_item(button.Button(style=disnake.ButtonStyle.secondary, label="Restart", custom_id=f"restart_server_{server_info['id']}"))
                view.add_item(button.Button(style=disnake.ButtonStyle.danger, label="Stop", custom_id=f"stop_server_{server_info['id']}"))
                view.add_item(button.Button(style=disnake.ButtonStyle.danger, label="Kill", custom_id=f"kill_server_{server_info['id']}"))

                await ctx.send(embed=embed, view=view)
        except requests.exceptions.RequestException as e:
            await ctx.send(f"⚠️ Unable to retrieve server information. Error: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(Server(bot))
