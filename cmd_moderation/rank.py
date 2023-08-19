import discord
from discord.ext import commands

async def get_roles(ctx: discord.AutocompleteContext):
    return [cat.name for cat in ctx.interaction.guild.roles]

class RankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="rank", description="Attribue un rôle spécifique à un membre")
    @commands.has_permissions(manage_roles=True)
    async def rank(ctx, member: discord.Member, *, role_name: discord.Option(str, autocomplete = discord.utils.basic_autocomplete(get_roles), required= True)):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        if role is None:
            await ctx.send(f"Le rôle '{role_name}' n'existe pas sur ce serveur.")
            return
        
        if role in member.roles:
            await ctx.send(f"{member.mention} a déjà le rôle '{role_name}'.")
            return
        
        try:
            await member.add_roles(role)
            await ctx.send(f"{member.mention} a reçu le rôle '{role_name}'.")
        except discord.Forbidden:
            await ctx.send("Je n'ai pas les permissions nécessaires pour attribuer des rôles.")