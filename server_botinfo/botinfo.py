import discord
from discord.ext import commands
from datetime import datetime
from discord import guild_only

class BotInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="botinfo", description="Donne des infos sur le bot")
    @guild_only()
    async def botinfo(self, ctx):
        latency = self.bot.latency * 1000
        embed = discord.Embed(title="Info du bot", description="Affiche les informations du bot", timestamp=datetime.now())
        embed.add_field(name="Nom du bot", value=f"{self.bot.user}")
        embed.add_field(name="Nombre de serveurs", value=f"{len(self.bot.guilds)} serveurs")
        embed.add_field(name="LATENCE DU BOT", value=f"{latency:.0f} ms", inline=False)
        await ctx.send(embed=embed)
