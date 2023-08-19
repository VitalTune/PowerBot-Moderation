import discord
from discord.ext import commands

from cmd_moderation import ban, banned_members, clear, member_list, unban, kick, member_count, create_channel, voice_mute, voice_unmute, delete_channel, delete_category, create_category, lock, unlock, deafen, slowmode, renew, warn, mute, unmute, rank, derank, userinfo
from server_botinfo import botinfo, ping
from commands import help, banner, create_embed, timer
from events import captcha, welcome, goodbye
import json
import traceback

with open("token.json", "r") as file:
    token = json.load(file)["token"]

# Initialisation du bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    latency = bot.latency * 1000
    print(f"The bot is logged as {bot.user} in {latency:.0f} ms")

@bot.event
async def on_command_error(ctx, error):
    error_traceback = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    print("\033[91m" + f"Error: {type(error).__name__} - {error}" + "\033[0m")
    print("\033[92m" + "Correction: (if available)" + "\033[0m")
    # Ajoutez ici les instructions pour afficher la correction pour chaque type d'erreur connu
    print("\033[93m" + "Traceback:" + "\033[0m")
    print(error_traceback)
    
    if isinstance(error, discord.ConnectionClosed) and error.code == 1006:
        print("\033[91m" + "Discord is not responding. Reason:" + "\033[0m")
        print(error.reason)

# Test.py
# bot.add_cog(test1.TestCog(bot))

bot.add_cog(ban.BanCog(bot))
bot.add_cog(clear.ClearCog(bot))
bot.add_cog(ping.PingCog(bot))
bot.add_cog(banned_members.BannedMembersCog(bot))
bot.add_cog(botinfo.BotInfoCog(bot))
bot.add_cog(member_list.MemberListCog(bot))
bot.add_cog(kick.KickCog(bot))
bot.add_cog(kick.KickedCog(bot))
bot.add_cog(unban.UnbanCog(bot))
bot.add_cog(banner.BannerCog(bot))
bot.add_cog(help.HelpCog(bot))
bot.add_cog(member_count.MemberCountCog(bot))
bot.add_cog(create_channel.CreateChannelCog(bot))
bot.add_cog(voice_mute.VoiceMuteCog(bot))
bot.add_cog(voice_unmute.VoiceUnmuteCog(bot))
bot.add_cog(delete_channel.DeleteChannelCog(bot))
bot.add_cog(delete_category.DeleteCategoryCog(bot))
bot.add_cog(create_category.CreateCategoryCog(bot))
bot.add_cog(lock.LockCog(bot))
bot.add_cog(unlock.UnlockCog(bot))
bot.add_cog(slowmode.SlowModeCog(bot))
bot.add_cog(slowmode.SlowModeStateCog(bot))
bot.add_cog(renew.RenewCog(bot))
bot.add_cog(captcha.CaptchaCog(bot))
bot.add_cog(captcha.SetCaptchaCog(bot))
set_welcome_cog = welcome.SetWelcomeCog(bot)
welcome_cog = welcome.WelcomeCog(bot, set_welcome_cog)
bot.add_cog(set_welcome_cog)
bot.add_cog(welcome_cog)
set_goodbye_cog = goodbye.SetGoodbyeCog(bot)
goodbye_cog = goodbye.GoodbyeCog(bot, set_goodbye_cog)
bot.add_cog(set_goodbye_cog)
bot.add_cog(goodbye_cog)
bot.add_cog(create_embed.EmbedCog(bot))
bot.add_cog(timer.TimerCog(bot))
bot.add_cog(warn.WarnCog(bot))
bot.add_cog(warn.WarningsCog(bot))
bot.add_cog(deafen.DeafenCog(bot))
bot.add_cog(rank.RankCog(bot))
bot.add_cog(derank.DerankCog(bot))
bot.add_cog(userinfo.UserInfoCog(bot))
bot.run(token)