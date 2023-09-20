import disnake
from disnake.ext import commands

from utils.var import *
from utils.error import *

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ HELP ⚙️ ==========')
        print('🔩 /help has been loaded')
        print()

    @commands.slash_command(name="help", description="See all the commands of the bot and how to use them")
    async def help(self, ctx):
        try:
            embed = disnake.Embed(
                title="List of commands",
                description="Here you wan find all the commands of the bot and their us",
                color=disnake.Color.green()
            )

            for command in self.bot.slash_commands:
                if command.description is None:
                    descr = "```Unknown```"
                else:
                    descr = f"```{command.description}```"
                
                embed.add_field(
                    name=f"**{self.bot.command_prefix}{command.name}**",
                    value=descr,
                    inline=False
                )

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=error_embed(e))

def setup(bot):
    bot.add_cog(HelpCog(bot))
