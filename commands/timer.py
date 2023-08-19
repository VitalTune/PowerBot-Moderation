import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class TimerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="timer", description="Pour définir un timer")
    async def timer(self, ctx, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
        total_seconds = self.calculate_total_seconds(years, months, days, hours, minutes, seconds)
        if total_seconds <= 0:
            await ctx.respond("Le temps doit être supérieur à zéro.")
            return

        embed = discord.Embed(title=f"Timer de {self.format_time(total_seconds)}", description=f"Temps restant: {self.format_time(total_seconds)}")

        message = await ctx.respond(embed=embed)

        while total_seconds > 0:
            await asyncio.sleep(1)
            total_seconds -= 1
            embed.description = f"Temps restant: {self.format_time(total_seconds)}"
            await message.edit_original_response(embed=embed)

        await ctx.respond(f"Le timer de {self.format_time(total_seconds)} est terminé.")

    def calculate_total_seconds(self, years, months, days, hours, minutes, seconds):
        total_seconds = 0
        if years:
            total_seconds += years * 365 * 24 * 60 * 60
        if months:
            total_seconds += months * 30 * 24 * 60 * 60
        if days:
            total_seconds += days * 24 * 60 * 60
        if hours:
            total_seconds += hours * 60 * 60
        if minutes:
            total_seconds += minutes * 60
        if seconds:
            total_seconds += seconds
        return total_seconds

    def format_time(self, total_seconds):
        remaining_time = timedelta(seconds=total_seconds)
        remaining_days = remaining_time.days
        remaining_years, remaining_days = divmod(remaining_days, 365)
        remaining_hours, remaining_minutes = divmod(remaining_time.seconds // 60, 60)
        remaining_minutes, remaining_seconds = divmod(remaining_minutes, 60)
        formatted_time = []
        if remaining_years:
            formatted_time.append(f"{remaining_years} an{'s' if remaining_years > 1 else ''}")
        if remaining_days:
            formatted_time.append(f"{remaining_days} jour{'s' if remaining_days > 1 else ''}")
        if remaining_hours:
            formatted_time.append(f"{remaining_hours} heure{'s' if remaining_hours > 1 else ''}")
        if remaining_minutes:
            formatted_time.append(f"{remaining_minutes} minute{'s' if remaining_minutes > 1 else ''}")
        if remaining_seconds:
            formatted_time.append(f"{remaining_seconds} seconde{'s' if remaining_seconds > 1 else ''}")
        return ", ".join(formatted_time)
