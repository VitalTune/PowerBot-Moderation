import discord
from discord.ext import commands

class DeafenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="deafen", description="Rendre un membre sourd dans un canal vocal")
    @commands.has_permissions(deafen_members=True)
    async def deafen(self, ctx, member: discord.Member):
        if ctx.author.voice is None:
            await ctx.respond("Vous devez être dans un canal vocal pour utiliser cette commande.")
            return
        
        if member.voice is None:
            await ctx.respond("Le membre spécifié n'est pas dans un canal vocal.")
            return
        
        await member.edit(deafen=True)
        await ctx.respond(f"{member.display_name} a été rendu sourd dans le canal vocal.")