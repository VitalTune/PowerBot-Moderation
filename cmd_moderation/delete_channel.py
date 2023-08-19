import discord
from discord.ext import commands
from discord import guild_only

async def get_channels(ctx: discord.AutocompleteContext):
    return [channel.name for channel in ctx.interaction.guild.channels if type(channel) != discord.CategoryChannel]

class DeleteChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="delete_channel", description="Permet de supprimer un salon")
    @guild_only()
    async def delete_channel(self, ctx, name: discord.Option(str, autocomplete = discord.utils.basic_autocomplete(get_channels), required= True)):
        channel = discord.utils.get(ctx.guild.channels, name=name)
        
        if channel is None:
            await ctx.respond(f"Le salon `{name}` n'existe pas.")
            return
        
        await channel.delete()
        await ctx.respond(f"Le salon `{name}` a été supprimé.")