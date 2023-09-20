import disnake
from disnake.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="See all the commands of the bot and how to use them")
    async def help(self, ctx):
        embed = disnake.Embed(
            title="List of commands",
            description="Here you wan find all the commands of the bot and their us",
            color=disnake.Color.green()
        )

        for command in self.bot.slash_commands:
            embed.add_field(
                name=f"**{self.bot.prefix}{command.name}**",
                value=command.help or "```Unknown```",
                inline=False
            )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))
