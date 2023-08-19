import discord
from discord.ext import commands
import sqlite3
from discord import guild_only
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("kicks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS kicks (
                user_id INTEGER PRIMARY KEY,
                reason TEXT
            )
            """
        )
        self.conn.commit()

    def get_kicks(self):
        self.cursor.execute("SELECT user_id, reason FROM kicks")
        kicks = self.cursor.fetchall()
        return kicks

database = Database()

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="kick", description="Pour kick un utilisateur")
    @commands.has_permissions(kick_members=True)
    @guild_only()
    async def kick(self, ctx, user: discord.Member, *, reason):
        await user.send(f"Tu vas être kick du serveur pour la raison suivante : `{reason}`\n**Tu peux revenir à tout moment mais tu vas devoir aller en detox avant de revenir, sinon ce sera un ban à vie**")
        await user.kick(reason=reason)
        database.add_kick(user.id, reason)
        
        embed = discord.Embed(title="Le juge a prononcé la peine moyenne, qui est un kick")
        embed.add_field(name="Membre kické", value=f"{user.mention}")
        embed.add_field(name="Nom du juge", value=f"{ctx.author.mention}")
        embed.add_field(name="Raison", value=f"{reason}")
        embed.set_footer(text="Il peut revenir à tout moment mais va falloir aller en detox")
        embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/7930-omen-kick.png")
        await ctx.send(embed=embed)

class KickedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="kicked", description="Affiche la liste des membres kickés")
    async def kicked(self, ctx):
        kicks = database.get_kicks()
        kick_count = len(kicks)
        
        if kick_count == 0:
            await ctx.send("Aucun membre n'a été kické sur ce serveur.")
            return
        
        kick_list = "\n".join([f"**Membre**: <@{kick[0]}> | **Raison**: {kick[1]}" for kick in kicks])
        
        embed = discord.Embed(title="Membres Kickés")
        embed.add_field(name="Nombre total de membres kickés", value=f"{kick_count}")
        embed.add_field(name="Liste des membres kickés", value=kick_list, inline=False)
        
        await ctx.respond(embed=embed)