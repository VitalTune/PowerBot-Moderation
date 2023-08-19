import discord
from discord.ext import commands

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="ban", description="Pour bannir un utilisateur")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, reason=None):
        if reason is None:
            reason = "Aucune raison spécifiée."
            
        await user.ban(reason=reason)
        embed = discord.Embed(title="Le juge a prononcé la peine maximale, qui est un ban à vie")
        embed.add_field(name="Membres bannis", value=f"{user}")
        embed.add_field(name="Nom du juge", value=f"{ctx.author}")
        embed.add_field(name="Raison", value=f"{reason}")
        embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5128-ban.png")
        await ctx.send(embed=embed)