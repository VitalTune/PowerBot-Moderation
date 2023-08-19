import discord
from discord.ext import commands
from discord import guild_only

class CreateCategoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="create_category", description="Permet de créer une categories")
    @guild_only()
    async def delete_categories(self, ctx, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        
        await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.respond(f"La categorie `{name}` a été créer avec succès.")
    