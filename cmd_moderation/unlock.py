import discord
from discord.ext import commands
from discord import guild_only


async def get_channels(ctx: discord.AutocompleteContext):
    return [channel.name for channel in ctx.interaction.guild.channels if type(channel) != discord.CategoryChannel]

class UnlockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="unlock", description="Pour débloquer le salon pour tous les membres")
    @guild_only()
    async def unlock_channel(self, ctx, name: discord.Option(str, autocomplete = discord.utils.basic_autocomplete(get_channels), required=True)):
        channel = discord.utils.get(ctx.guild.channels, name=name)
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.respond(f"{ctx.channel.mention} a été unlock.")