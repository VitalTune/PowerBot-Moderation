import discord
from discord.ext import commands
from discord import guild_only


class VoiceUnmuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="voice_unmute", description="Pour demuter une personne muter dans un salon vocal")
    @guild_only()
    async def voice_unmute(self, ctx, member: discord.Member):
        if not member.voice:
            await ctx.respond("L'utilisateur n'est dans aucun salon vocal.")
        elif not member.voice.mute:
            await ctx.respond(f"{member.mention} n'est pas muté.")
        else:
            await member.edit(mute=False)
            await ctx.respond(f"{member.mention} a été demuté.")
