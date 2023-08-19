import discord
from discord.ext import commands


class SetWelcomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.welcome_enabled = False
        self.welcome_message = None
        self.welcome_channel = None

    @commands.slash_command(name="set_welcome", description="Définit le message de bienvenue et le salon")
    async def set_welcome(self, ctx):
        first = await ctx.send("Veuillez entrer le message de bienvenue (texte uniquement) :")
        message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        self.welcome_message = message.content
        await first.delete()

        second = await ctx.send("Veuillez mentionner le salon où le message de bienvenue sera envoyé :")
        channel = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        channel_id = int(channel.content[2:-1])  # Extract the channel ID from the mention
        welcome_channel = self.bot.get_channel(channel_id)
        await second.delete()
        if welcome_channel:
            self.welcome_channel = welcome_channel
            self.welcome_enabled = True
            await ctx.send("La fonction de bienvenue a été activée et configurée avec succès.", delete_after = 3)
        else:
            await ctx.send("Le salon spécifié est invalide. Veuillez réessayer.", delete_after = 3)

class WelcomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot, set_welcome_cog: SetWelcomeCog):
        self.bot = bot
        self.set_welcome_cog = set_welcome_cog

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.set_welcome_cog.welcome_enabled:
            embed = discord.Embed(title="Bienvenue sur le serveur !", description=self.set_welcome_cog.welcome_message, color=0x7289DA)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Pseudo", value=member.display_name, inline=False)
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.set_footer(text=f"Nous sommes maintenant {len(member.guild.members)} membres sur le serveur.")

            await self.set_welcome_cog.welcome_channel.send(embed=embed)