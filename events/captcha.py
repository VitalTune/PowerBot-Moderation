import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import random
import asyncio
import io

class SetCaptchaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="set_captcha", description="Pour définir votre captcha")
    async def set_captcha(self, ctx):
        # Demander le salon du captcha
        message1 = await ctx.respond("Veuillez mentionner le salon du captcha.")
        try:
            message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
            captcha_channel = message.channel_mentions[0]

            await message.delete()  # Supprimer le message de demande
            await message1.delete_original_response()
        except (IndexError, asyncio.TimeoutError):
            await ctx.send("Salon du captcha invalide.")
            await message1.delete()
            return
        
        # Demander la difficulté du captcha de 1 à 10
        message2 = await ctx.send("Veuillez choisir la difficulté du captcha de 1 à 10.")
        try:
            message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
            difficulty = int(message.content)
            if difficulty < 1 or difficulty > 10:
                raise ValueError
            await message.delete()  # Supprimer le message de demande
            await message2.delete()
        except (ValueError, asyncio.TimeoutError):
            await ctx.send("Difficulté du captcha invalide.")
            await message2.delete()
            return
        
        captcha_cog = self.bot.get_cog("CaptchaCog")
        if captcha_cog is None:
            captcha_cog = CaptchaCog(self.bot)
            self.bot.add_cog(captcha_cog)
        
        captcha_cog.set_configuration(captcha_channel, difficulty)
        succes_message = await ctx.send("Configuration du captcha terminée.")
        await asyncio.sleep(5)  # Attendre 5 secondes
        await succes_message.delete()


class CaptchaCog(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.chances = {}
        self.font = ImageFont.truetype("arial.ttf", 30)
        self.captcha_channel = None
        self.difficulty = 1
    
    def set_configuration(self, captcha_channel, difficulty):
        self.captcha_channel = captcha_channel
        self.difficulty = difficulty
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.captcha_channel is None:
            return
        
        captcha_role = discord.utils.get(member.guild.roles, name="Captcha")
        if not captcha_role:
            captcha_role = await member.guild.create_role(name="Captcha")
        
        await member.add_roles(captcha_role)
        captcha_image = self.generate_captcha()
        self.chances[member.id] = 3
        message = await self.captcha_channel.send(f"{member.mention}, veuillez résoudre ce captcha pour rejoindre le serveur:", file=captcha_image)
        await message.delete(delay=60)  # Supprimer le message après 60 secondes
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel == self.captcha_channel:
            if message.author.id in self.chances:
                if message.content == self.captcha_text:
                    member = message.guild.get_member(message.author.id)
                    captcha_role = discord.utils.get(member.guild.roles, name="Captcha")
                    await member.remove_roles(captcha_role)
                    del self.chances[member.id]
                    await message.channel.send("Captcha résolu ! Bienvenue sur le serveur.")
                    await message.delete()  # Supprimer le message de résolution du captcha
                    await self.delete_captcha_images(member)
                else:
                    self.chances[message.author.id] -= 1
                    if self.chances[message.author.id] == 0:
                        member = message.guild.get_member(message.author.id)
                        await member.kick(reason="Échec du captcha")
                        del self.chances[member.id]
                        await message.channel.send("Vous avez raté le captcha trop de fois. Vous avez été expulsé du serveur.")
                        await message.delete()  # Supprimer le message d'échec du captcha
                        await self.delete_captcha_images(member)
                    else:
                        await message.channel.send(f"Captcha incorrect. Il vous reste {self.chances[message.author.id]} chances.")
                        await message.delete()  # Supprimer le message de réponse au captcha
    
    def generate_captcha(self):
        captcha_length = 6 * self.difficulty  # Multiplier la longueur du captcha par la difficulté
        captcha_text = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=captcha_length))
        self.captcha_text = captcha_text
        image = Image.new("RGB", (200, 100), "white")
        draw = ImageDraw.Draw(image)
        font_size = self.font.getsize(captcha_text)
        draw.text((100 - font_size[0] / 2, 50 - font_size[1] / 2), captcha_text, font=self.font, fill="black")
        for i in range(1000):
            draw.point((random.randint(0, 199), random.randint(0, 99)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        captcha_image_bytes = io.BytesIO()
        image.save(captcha_image_bytes, format="PNG")
        captcha_image_bytes.seek(0)
        return discord.File(captcha_image_bytes, filename="captcha.png")
    
    async def delete_captcha_images(self, member):
        async for message in self.captcha_channel.history():
            if message.author == member and message.attachments:
                for attachment in message.attachments:
                    await attachment.delete()
                await message.delete()