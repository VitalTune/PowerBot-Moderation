import discord
from discord.ext import commands

class BannerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="banner", description="Affiche la bannière d'un utilisateur")
    async def banner(self, ctx, user: discord.User):
        embed = discord.Embed(title=f"Bannière de {user}", color=user.color)

        if user.banner:
            embed.set_image(url=user.banner.url)
        else:
            embed.description = "Cet utilisateur n'a pas de bannière."

        await ctx.respond(embed=embed)