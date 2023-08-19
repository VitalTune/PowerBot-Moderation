import discord
from discord.ext import commands, pages


class BannedMembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="banned-members", description="Affiche la liste complète des membres bannis du serveur avec un paginador")
    @commands.has_permissions(ban_members=True)    
    async def members_list(self, ctx: discord.ApplicationContext):
        guild_id = ctx.guild.id  # Obtenez l'ID du serveur Discord
        guild = self.bot.get_guild(guild_id)  # Obtenez l'instance de discord.Guild
        embeds = []
        page_xp = []
        count = 0
        async for ban_entry in guild.bans():            
            name = ban_entry.user
            embeds.append(f"`{count+1}.` **{name}** | `{ban_entry.user.id}`")
            count += 1
            if count % 10 == 0:
                page = discord.Embed(title="🏆 Members")
                for entry in embeds[-10:]:
                    page.add_field(name="** **", value=entry, inline = False)
                page_xp.append(page)
                embeds.clear()
        if embeds:
            page = discord.Embed(title="🏆 Members")
            for entry in embeds:
                page.add_field(name="** **", value=entry, inline = False)
            page_xp.append(page)
        if not page_xp:
            await ctx.send("Il n'y a pas de membres bannis sur ce serveur.")
            return
        paginator = pages.Paginator(pages=page_xp)
        await paginator.respond(ctx.interaction, ephemeral=False)
