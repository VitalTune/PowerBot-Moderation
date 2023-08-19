import discord
from discord.ext import commands
from discord import guild_only

class UserInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="user-info", description="Afficher les informations d'un utilisateur")
    @guild_only()
    async def user_info(self, ctx, member: discord.Member):
        embed = discord.Embed(title="Informations sur l'utilisateur", color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Nom", value=member.name, inline=True)
        embed.add_field(name="Surnom", value=member.nick, inline=True)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Statut", value=str(member.status).capitalize(), inline=True)
        embed.add_field(name="Rôle(s)", value=", ".join([role.mention for role in member.roles[1:]]), inline=False)
        embed.set_footer(text=f"Requête de {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.respond(embed=embed)