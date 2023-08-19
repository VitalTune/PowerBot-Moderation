import discord
from discord.ext import commands
from discord import guild_only

class SlowModeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set_slowmode", description="Définit le mode lent pour un salon")
    @commands.has_permissions(manage_channels=True)
    async def set_slowmode(self, ctx, hours: int = 0, minutes: int = 0, seconds: int = 0):
        time = (hours * 3600) + (minutes * 60) + seconds
        await ctx.channel.edit(slowmode_delay=time)
        await ctx.send(f"Le slowmode a été défini à {hours}h {minutes}m {seconds}s pour {ctx.channel.mention}.")

class SlowModeStateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slowmode_time = 0

    @commands.slash_command(name="slowmode_state", description="Active ou désactive le mode lent pour un salon")
    @guild_only()
    async def slowmode_state(self, ctx, mode: str):
        """Active ou désactive le slowmode pour le salon"""
        mode = mode.lower()
        if mode == "disable":
            if ctx.channel.slowmode_delay == 0:
                await ctx.send(f"Le slowmode est déjà désactivé pour {ctx.channel.mention}.")
            else:
                self.slowmode_time = ctx.channel.slowmode_delay
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.send(f"Le slowmode a été désactivé pour {ctx.channel.mention}.")
        elif mode == "enable":
            if ctx.channel.slowmode_delay > 0:
                await ctx.send(f"Le slowmode est déjà activé pour {ctx.channel.mention} avec un temps de {self.format_time(ctx.channel.slowmode_delay)}.")
            else:
                time = self.slowmode_time if self.slowmode_time > 0 else None
                await ctx.channel.edit(slowmode_delay=time)
                if time:
                    await ctx.send(f"Le slowmode a été activé pour {ctx.channel.mention} avec un temps de {self.format_time(time)}.")
                else:
                    await ctx.send(f"Le slowmode a été activé pour {ctx.channel.mention} mais aucun temps n'a été spécifié.")

    def format_time(self, seconds):
        """Convertit des secondes en une chaîne de temps formatée"""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours}h {minutes}m {seconds}s"
