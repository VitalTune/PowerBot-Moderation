import discord
from discord.ext import commands
from discord import guild_only

async def get_categories(ctx: discord.AutocompleteContext):
    return [cat.name for cat in ctx.interaction.guild.categories]

class DeleteCategoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="delete_category", description="Permet de supprimer une categories")
    @guild_only()
    async def delete_categories(self, ctx, name: discord.Option(str, autocomplete = discord.utils.basic_autocomplete(get_categories), required= True)):
        category = discord.utils.get(ctx.guild.categories, name=name)
        
        if category is None:
            await ctx.respond(f"La categorie `{name}` n'existe pas.")
            return
        
        await category.delete()
        await ctx.respond(f"La categorie `{name}` a été supprimé.")