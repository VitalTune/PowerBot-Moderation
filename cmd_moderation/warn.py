import discord
from discord.ext import commands
import sqlite3
import os

if not os.path.exists("Data"):
    os.makedirs("Data")

conn = sqlite3.connect('Data/warn_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS warn_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id INTEGER,
                server_name TEXT,
                server_invite TEXT,
                server_owner_id INTEGER,
                server_owner_name TEXT,
                warn_giver_id INTEGER,
                warn_giver_name TEXT,
                warn_target_id INTEGER,
                warn_target_name TEXT,
                warn_count INTEGER,
                reason TEXT
)''')

conn.commit()

cursor.execute("SELECT server_id, warn_target_id, warn_count, reason FROM warn_db")
result = cursor.fetchall()

warnings = {}
for server_id, target_id, count, reason in result:
    if server_id not in warnings:
        warnings[server_id] = {}
    warnings[server_id][target_id] = (count, reason)

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="warn", description="Permet de donner un avertissement")
    async def warn(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        if ctx.author.guild_permissions.manage_messages:
            invites = await ctx.guild.invites()
            invite = invites[0] if invites else await ctx.channel.create_invite()

            try:
                cursor.execute('''INSERT INTO warn_db (server_id, server_name, server_invite, server_owner_id, 
                                                        server_owner_name, warn_giver_id, warn_giver_name, 
                                                        warn_target_id, warn_target_name, warn_count, reason) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (ctx.guild.id, ctx.guild.name, f"discord.gg/{invite.code}", 
                                ctx.guild.owner_id, str(ctx.guild.owner), ctx.author.id, str(ctx.author), 
                                member.id, str(member), warnings.get(ctx.guild.id, {}).get(member.id, (0, []))[0] + 1, reason))
                conn.commit()

                if ctx.guild.id not in warnings:
                    warnings[ctx.guild.id] = {}
                if member.id not in warnings[ctx.guild.id]:
                    warnings[ctx.guild.id][member.id] = (0, []) 
                warnings[ctx.guild.id][member.id] = (warnings[ctx.guild.id][member.id][0] + 1,
                                                     warnings[ctx.guild.id][member.id][1] + [reason])

                await ctx.respond(f"{member.mention} a été averti pour : {reason}", ephemeral=True)
            except Exception as e:
                await ctx.respond("Une erreur est survenue lors de l'enregistrement de l'avertissement.", ephemeral=True)
                print(e)
        else:
            await ctx.respond("Vous n'avez pas les permissions pour donner un avertissement.", ephemeral=True)

class WarningsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="warnings", description="Permet d'afficher le nombre d'avertssement d'un membre")
    async def warnings(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_messages:
            server_warnings = warnings.get(ctx.guild.id, {})
            member_warnings = server_warnings.get(member.id, None)

            if member_warnings:
                embed = discord.Embed(title=f"Avertissements de {member.display_name}", color=0xFF0000)
                embed.set_author(name=member.name, icon_url=member.avatar.url)
                embed.description = f"{member.mention} a {member_warnings[0]} avertissement(s)."

                for i, reason in enumerate(member_warnings[1], start=1):
                    embed.add_field(name=f"Avertissement {i}", value=f"Raison : {reason}", inline=False)

                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title = "Warnings Pannel")
                embed.description = f"{member.mention} n'a pas d'avertissements."
                await ctx.respond(embed = embed)
        else:
            await ctx.respond("❌ Vous n'avez pas les permissions pour voir les avertissements.")
