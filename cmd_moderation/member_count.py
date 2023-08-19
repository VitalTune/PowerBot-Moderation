import discord
from discord.ext import commands
from discord import guild_only



class MemberCountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name = "member_counts", description = "Affiche le nombre de membre dans le serveur")
    @guild_only()
    async def member_counts(self, ctx):
        guild_id = ctx.guild.id
        guild = self.bot.get_guild(guild_id)
        embed = discord.Embed(title = f"Il y a {guild.member_count} membres sur ce serveur.")
        await ctx.respond(embed = embed)