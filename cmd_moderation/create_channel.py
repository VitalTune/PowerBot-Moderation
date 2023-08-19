import discord
from discord.ext import commands
from discord import guild_only

async def get_categories(ctx: discord.AutocompleteContext):
    return [cat.name for cat in ctx.interaction.guild.categories]

class CreateChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="create_channel", description="Permet de créer des salons")
    @guild_only()
    async def create_channel(self, ctx, name, category: discord.Option(str, autocomplete = discord.utils.basic_autocomplete(get_categories), required= False)):
        if name is None:
            await ctx.send("Veuillez spécifier un nom de salon.")
            return
        
        if category is None:
            category = None
        else:
            category = discord.utils.get(ctx.guild.categories, name=category)
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        
        await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=category)
        
        if category is None:
            await ctx.respond(f"Le salon `{name}` a été créé sans catégorie.")
        else:
            await ctx.respond(f"Le salon `{name}` a été créé dans la catégorie `{category.name}`.")
