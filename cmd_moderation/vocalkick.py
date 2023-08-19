import discord
from discord.ext import commands

class VocalKickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="voice-kick", description="Exclut l'utilisateur sélectionné du salon vocal")
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, user: discord.Member):
        """Exclut l'utilisateur sélectionné du salon vocal"""
        voice_state = user.voice
        if voice_state and voice_state.channel:  # Check if the user is in a voice channel
            try:
                await voice_state.disconnect()
                await ctx.respond(f"{user.mention} a été exclu du salon vocal avec succès !")
            except discord.Forbidden:
                await ctx.respond("Je n'ai pas la permission de le faire.")
            except Exception as e:
                await ctx.respond(f"Une erreur s'est produite : {e}")
        else:
            await ctx.respond(f"{user.mention} n'est pas dans un salon vocal !")