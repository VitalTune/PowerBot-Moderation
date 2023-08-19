import discord
from discord.ext import commands
from discord import guild_only


class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="clear", description="Supprimer un nombre donné de message")
    @guild_only()
    async def clear(self, ctx, nombre):
        messages_deleted = await ctx.channel.purge(limit=int(nombre), bulk=True)
        await ctx.respond(f"{len(messages_deleted)} messages ont été supprimés avec succès", delete_after=5)
