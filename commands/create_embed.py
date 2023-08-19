import discord
from discord.ext import commands
import asyncio

class EmbedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="create_embed", description="Crée un embed interactif")
    async def create_embed(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            await ctx.respond("Veuillez entrer le titre de l'embed :")
            title_msg = await self.bot.wait_for('message', check=check, timeout=60)
            title = title_msg.content
            await title_msg.delete()

            await ctx.send("Voulez-vous ajouter une description à l'embed ? (Oui/Non)")
            confirmation_msg = await self.bot.wait_for('message', check=check, timeout=60)
            confirmation_content = confirmation_msg.content.lower()
            await confirmation_msg.delete()

            description = None
            if confirmation_content == "oui":
                await ctx.send("Veuillez entrer la description de l'embed :")
                description_msg = await self.bot.wait_for('message', check=check, timeout=60)
                description = description_msg.content
                await description_msg.delete()

            await ctx.send("Voulez-vous ajouter une couleur à l'embed ? (Oui/Non)")
            confirmation_msg = await self.bot.wait_for('message', check=check, timeout=60)
            confirmation_content = confirmation_msg.content.lower()
            await confirmation_msg.delete()

            color = discord.Color.default()
            if confirmation_content == "oui":
                await ctx.send("Veuillez entrer le nom de la couleur (par exemple : rouge, bleu, vert) :")
                color_name_msg = await self.bot.wait_for('message', check=check, timeout=60)
                color = self.get_color(color_name_msg.content)
                await color_name_msg.delete()

            await ctx.send("Voulez-vous ajouter des champs à l'embed ? (Oui/Non)")
            confirmation_msg = await self.bot.wait_for('message', check=check, timeout=60)
            confirmation_content = confirmation_msg.content.lower()
            await confirmation_msg.delete()

            fields = []
            if confirmation_content == "oui":
                add_fields = True
                while add_fields:
                    await ctx.send("Veuillez entrer le nom du champ :")
                    field_name_msg = await self.bot.wait_for('message', check=check, timeout=60)
                    field_name = field_name_msg.content
                    await field_name_msg.delete()

                    await ctx.send("Veuillez entrer la valeur du champ :")
                    field_value_msg = await self.bot.wait_for('message', check=check, timeout=60)
                    field_value = field_value_msg.content
                    await field_value_msg.delete()

                    fields.append((field_name, field_value))

                    await ctx.send("Voulez-vous ajouter un autre champ ? (Oui/Non)")
                    confirmation_msg = await self.bot.wait_for('message', check=check, timeout=60)
                    confirmation_content = confirmation_msg.content.lower()
                    await confirmation_msg.delete()

                    if confirmation_content != "oui":
                        add_fields = False

            await ctx.send("Voulez-vous ajouter une image à l'embed ? (Oui/Non)")
            confirmation_msg = await self.bot.wait_for('message', check=check, timeout=60)
            confirmation_content = confirmation_msg.content.lower()
            await confirmation_msg.delete()

            image_url = None
            if confirmation_content == "oui":
                await ctx.send("Veuillez envoyer l'image à ajouter :")
                image_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.attachments, timeout=60)
                attachment = image_msg.attachments[0]
                image_url = attachment.url
                await image_msg.delete()

            embed = discord.Embed(title=title, description=description, color=color)

            for field in fields:
                embed.add_field(name=field[0], value=field[1], inline=False)

            if image_url:
                embed.set_image(url=image_url)

            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. Veuillez recommencer la commande.")

    def get_color(self, color_name):
        colors = {
            "rouge": discord.Color.red(),
            "bleu": discord.Color.blue(),
            "vert": discord.Color.green(),
            "jaune": discord.Color.yellow(),
            "violet": discord.Color.purple(),
            "mauve": discord.Color.purple(),
            "gris": discord.Color.dark_gray()
            # Ajoutez d'autres couleurs et noms associés ici
        }
        return colors.get(color_name.lower(), discord.Color.default())