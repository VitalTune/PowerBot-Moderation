import discord
from discord.ext import commands
from discord import guild_only

class UnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="unban", description="Pour débannir un utilisateur")
    @guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason="Aucune raison spécifiée"):
        banned_users = await ctx.guild.bans()
        
        for ban_entry in banned_users:
            if ban_entry.user == user:
                await ctx.guild.unban(user, reason=reason)
                await ctx.send(f"{user} a été débanni du serveur pour la raison suivante :\n```{reason}```")
                return
        
        await ctx.send(f"L'utilisateur {user} n'est actuellement pas banni du serveur.")