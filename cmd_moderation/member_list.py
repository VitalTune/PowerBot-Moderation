import discord
from discord.ext import commands, pages
from discord import guild_only

class MemberListCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="member-list", description="Affiche la liste complète des membres bannis du serveur avec un paginador")
    @guild_only()
    async def members_list(self, ctx: discord.ApplicationContext):
        embeds = []
        page_xp = []
        count = 0
        for member in ctx.guild.members:
            name = member.name
            embeds.append(f"`{count+1}.` **{name}** | `{member.id}`")
            count += 1
            if count % 10 == 0:
                page = discord.Embed(title="🏆 Members")
                for entry in embeds[-10:]:
                    page.add_field(name=" ", value=entry, inline=False)
                page_xp.append(page)
                embeds = []

        if len(embeds) > 0:
            page = discord.Embed(title="🏆 Members")
            for entry in embeds:
                page.add_field(name=" ", value=entry, inline=False)
            page_xp.append(page)

        if len(page_xp) > 0:
            paginator = pages.Paginator(pages=page_xp)
            await paginator.respond(ctx.interaction, ephemeral=False)
        else:
            await ctx.send("> Aucune donnée à afficher.")
