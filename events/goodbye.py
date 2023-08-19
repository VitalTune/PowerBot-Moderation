import discord
from discord.ext import commands


class SetGoodbyeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.goodbye_enabled = False
        self.goodbye_message = None
        self.goodbye_channel = None

    @commands.slash_command(name="set_goodbye", description="Définit le message d'aurevoir et le salon")
    async def set_goodbye(self, ctx):
        await ctx.send("Veuillez entrer le message d'aurevoir (texte uniquement) :")
        message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        self.goodbye_message = message.content

        await ctx.send("Veuillez mentionner le salon où le message d'aurevoir sera envoyé :")
        channel = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        channel_id = int(channel.content[2:-1])  # Extract the channel ID from the mention
        goodbye_channel = self.bot.get_channel(channel_id)

        if goodbye_channel:
            self.goodbye_channel = goodbye_channel
            self.goodbye_enabled = True
            await ctx.send("La fonction d'aurevoir a été activée et configurée avec succès.")
        else:
            await ctx.send("Le salon spécifié est invalide. Veuillez réessayer.")


class GoodbyeCog(commands.Cog):
    def __init__(self, bot: commands.Bot, set_goodbye_cog: SetGoodbyeCog):
        self.bot = bot
        self.set_goodbye_cog = set_goodbye_cog

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.set_goodbye_cog.goodbye_enabled:
            goodbye_message = self.set_goodbye_cog.goodbye_message.format(member=member)
            await self.set_goodbye_cog.goodbye_channel.send(goodbye_message)
