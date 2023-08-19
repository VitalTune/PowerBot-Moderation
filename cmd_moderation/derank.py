import discord
from discord.ext import commands

async def get_roles(ctx: discord.AutocompleteContext):
    return [cat.name for cat in ctx.interaction.guild.roles]

class DerankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="derank", description="Retire un rôle spécifique à un membre")
    @commands.has_permissions(manage_roles=True)
    async def derank(self, ctx, member: discord.Member, role: discord.Option(str, autocomplete = discord.utils.basic_autocomplete(get_roles), required= True)):
        if role not in member.roles:
            await ctx.respond(f"{member.display_name} n'a pas le rôle {role.name}.")
            return
        
        await member.remove_roles(role)
        await ctx.respond(f"{member.display_name} a été déclassé et le rôle {role.name} lui a été retiré.")