import discord
from discord.ext import commands, pages
from discord.commands import SlashCommandGroup

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            discord.Embed(title="Moderation"),
            discord.Embed(title="Page 3"),
            discord.Embed(title="Page 3"),
            discord.Embed(title="Page 3"),
            discord.Embed(title="Page 3")             
        ]
        self.pages[0].add_field(name="ban", value="Permet de bannir un membre\n`/ban [member_name]`", inline=False)
        self.pages[0].add_field(name="unban", value="Permet de débannir un membre\n`/unban [member_name]`", inline=False)
        self.pages[0].add_field(name="banned_member", value="Affiche une liste ds membres banni du serveur", inline=False)
        self.pages[0].add_field(name="kick", value="Permet d'exclure quelqu'un\n`/kick [member_name]`", inline=False)
        self.pages[0].add_field(name="clear", value="Permet de supprimer un nombre donné de message\n`/clear [number_of_message]`", inline=False)
        self.pages[0].add_field(name="member_list", value="Permet de donner la liste des membres\n`/member_list`", inline=False)
        self.pages[0].add_field(name="lock", value="Permet de verrouiller un salon afin que les rôles non autorisés ne puissent écrire\n`/lock [channel_name]` **ou** `/lock` (Il faut écrire la commande dans le salon qu'on veut verrouiller)", inline=False)
        self.pages[0].add_field(name="unlock", value="Permet de déverrouiller un salon afin que les rôles non autorisés puissent écrire\n`/unlock [channel_name]` **ou** `/unlock` (Il faut écrire la commande dans le salon qu'on veut verrouiller)", inline=False)
        self.pages[0].add_field(name="member_count", value="Permet d'afficher le nombre de membres dans le serveur\n`/member_count`", inline=False)
        self.pages[0].add_field(name="mute", value="Permet de mute un membre en le privant de tout salon (sauf le salon prion qui sera ajouté automatiquement dès le premier mute) et donner un temps de mute au membre\n/mute [member_name] [time_mute]", inline=False)
        self.pages[0].add_field(name="unmute", value="Permet de demute un membre en lui redonnant l'accès à tous les salons (si le temps de mute est écoulé cela affichera un message d'erreur)\n`/unmute [member_name]`\n**__:warning: Si la commande est exécutée sans argument, tous les membres mute seront demute__**", inline=False)
        self.pages[0].add_field(name="rank", value="Permet de donner un rôle à un membre (Possibilité de donner directement des rôles mais le bot premium est requis : __En cours de création__\nExample : `/rank perm1/perm2/perm3/..../perm *`\n\n`/rank [role_donner]`", inline=False)
        self.pages[0].add_field(name="userinfo", value="Permet d'afficher les informations de l'utilisateur\n`/userinfo [username]` (si le champ est laissé vide, les infos de l'utilisateur exécutant la commande seront affichées)", inline=False)
        self.pages[0].add_field(name="warn", value="Donne un avertissement à un membre\n`/warn [member_name] [raison] (si la raison n'est pas donnée, une erreur est envoyée)`", inline=False)
        self.pages[0].add_field(name="renew", value="Permet de renouveler un salon\n`/renew [channel_name]()` **ou** `/renew` (Il faut écrire la commande dans le salon qu'on veut renouveler)", inline=False)
        self.pages[0].add_field(name="Information supplémentaire :", value="J'ai oublié ce que je devais dire (c'est super important je crois donc s'il y a le moindre bug, signalez-le : `The Gost#8246`)", inline=False)
        
        # self.pages[1].add_field(name="1", value="2")
        # self.pages[2].add_field(name="1", value="2")
        # self.pages[3].add_field(name="1", value="2")
        # self.pages[4].add_field(name="1", value="2")
    def get_pages(self):
        return self.pages

    pagetest = SlashCommandGroup("pagetest", "Commands for testing ext.pages")

    @commands.slash_command(name="help", description = "Affiche de l'aire pour les commande du serveur")
    async def pagetest_default(self, ctx: discord.ApplicationContext):
        """Demonstrates using the paginator with the default options."""
        paginator = pages.Paginator(pages=self.get_pages())
        await paginator.respond(ctx.interaction, ephemeral=False)
