import discord
from discord.ext import commands

async def get_channels(ctx: discord.AutocompleteContext):
    return [channel.name for channel in ctx.interaction.guild.channels if isinstance(channel, discord.TextChannel)]

class RenewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="renew", description="Réinitialise un salon texte existant")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def reset_channel(self, ctx, name: str = discord.Option(description="Nom du salon à réinitialiser", autocomplete=get_channels, required=True)):
        channel = discord.utils.get(ctx.guild.channels, name=name)

        if channel is None:
            await ctx.respond(f"Le salon '{name}' n'a pas été trouvé sur ce serveur.")
            return

        overwrites = channel.overwrites
        position = channel.position
        category = channel.category

        await ctx.respond(f"Le salon {channel.mention} va être réinitialisé dans quelques instants...", ephemeral=True)
        
        await channel.delete()

        new_channel = await category.create_text_channel(name, overwrites=overwrites, position=position)

        await new_channel.send(f"Le salon {new_channel.mention} a été réinitialisé avec succès !", ephemeral=True)
