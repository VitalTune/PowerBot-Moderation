import discord
from discord.ext import commands

async def get_roles(ctx: discord.AutocompleteContext):
    return [cat.name for cat in ctx.interaction.guild.roles]

class RoleInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="rolesinfo", description="Affiche des informations sur un rôle")
    async def role_info(self, ctx, *, role_name: discord.Option(str, autocomplete = discord.utils.basic_autocomplete(get_roles), required= True)):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        if role is None:
            await ctx.send(f"Le rôle '{role_name}' n'a pas été trouvé sur ce serveur.")
            return
        
        role_permissions = role.permissions
        members_with_role = len(role.members)
        
        permissions_list = "\n".join([f"{perm}: {value}" for perm, value in role_permissions])
        
        embed = discord.Embed(
            title=f"Informations sur le rôle {role.name}",
            description=f"ID du rôle: {role.id}\nMembres avec ce rôle: {members_with_role}",
            color=role.color
        )
        embed.add_field(name="Permissions", value=permissions_list, inline=False)
        
        await ctx.send(embed=embed)