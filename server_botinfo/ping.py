import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="ping", description="Vérifie la latence du bot")
    async def ping(self, ctx):
        latence = self.bot.latency * 1000
        await ctx.respond(f"Ping....")
        await ctx.edit(content = f"Pong !🏓 \nLatence : {latence:.0f} ms")