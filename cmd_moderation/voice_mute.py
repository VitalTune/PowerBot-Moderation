import discord
from discord.ext import commands
from discord import guild_only



class VoiceMuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="voice_mute", description="Pour muter des personnes dans un salon vocal")
    @guild_only()
    async def voice_mute(self, ctx, member: discord.Member):
        if not member.voice:
            await ctx.respond("L'utilisateur n'est dans aucun salon vocal.")
        elif member.voice.mute:
            await ctx.respond(f"{member.mention} est déjà muté.")
        else:
            await member.edit(mute=True)
            await ctx.respond(f"{member.mention} a été muté.")
