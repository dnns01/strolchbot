import os
import random
from abc import ABC
from time import sleep, time

from dotenv import load_dotenv
from twitchio.dataclasses import Context, Message, Channel
from twitchio.ext import commands

from giveaway_cog import GiveawayGog
from kaputt_cog import KaputtCog
from spotify_cog import SpotifyCog
from vote_cog import VoteCog

load_dotenv()


class StrolchiBot(commands.Bot, ABC):
    def __init__(self):
        self.IRC_TOKEN = os.getenv("IRC_TOKEN")
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.NICK = os.getenv("NICK")
        self.CHANNEL = os.getenv("CHANNEL")
        self.PREFIX = os.getenv("PREFIX")
        self.BATI_PROBABILITY = float(os.getenv("BATI_PROBABILITY"))
        self.BATI_KAPPA_PROBABILITY = float(os.getenv("BATI_KAPPA_PROBABILITY"))
        self.BATI_DELAY = int(os.getenv("BATI_DELAY"))
        self.last_bati = 0
        super().__init__(irc_token=self.IRC_TOKEN, prefix=self.PREFIX, nick=self.NICK, initial_channels=[self.CHANNEL],
                         client_id=self.CLIENT_ID,
                         client_secret=self.CLIENT_SECRET)
        self.add_cog(GiveawayGog(self))
        self.add_cog(VoteCog(self))
        self.add_cog(KaputtCog(self))
        self.add_cog(SpotifyCog(self))

    @staticmethod
    async def send_me(ctx, content, color):
        """ Change Text color to color and send content as message """

        if type(ctx) is Context or type(ctx) is Channel:
            await ctx.color(color)
            await ctx.send_me(content)
        elif type(ctx) is Message:
            await ctx.channel.color(color)
            await ctx.channel.send_me(content)

    async def event_ready(self):
        print('Logged in')

    @staticmethod
    def get_percentage(part, total):
        """ Calculate percentage """
        if total != 0:
            return round(part / total * 100, 1)

        return 0

    def channel(self):
        return self.get_channel(self.CHANNEL)

    async def chatters(self):
        return await self.get_chatters(self.CHANNEL)

    async def stream(self):
        return await self.get_stream(self.CHANNEL)


bot = StrolchiBot()


@bot.command(name="sounds")
async def cmd_sounds(ctx):
    await ctx.send(
        "Kenner*innen fahren folgende Manöver im Chat: 🔊 !achso , !andi , !arbeit , !asozial , !bah , !ban , !bier , !blueprint , !brüller , !channel , !chat , !coden , !content , !dinge , !dumm , !einbauen , !engine , !fail , !fckn , !follow 🔊")
    await ctx.send(
        "🔊 !gehtnicht , !geil , !gumo , !gumosuika , !guna , !heyhahaha , !humor , !hä , !indiemüll , !kaputt , !kommafenster , !käffchen , !langweilig , !maul , !mikkel , !naclear , !nenene , !oberscheiße , !opfer , !panne , !pinkler , !prost , !raus , !schödadudabi , !soklappts , !soklapptsnicht , !spiel , !suikasieht , !suikastolz , !teil , !topagent , !tröte , !utz , !wamaduda, !weißnicht , !äther 🔊")


@bot.listen("event_message")
async def bati(message):
    if message.author == "bati_mati":
        if ("kappa" in message.content.lower() and random.random() < bot.BATI_KAPPA_PROBABILITY) \
                or (random.random() < bot.BATI_PROBABILITY and time() >= bot.last_bati + (bot.BATI_DELAY * 3600)):
            sleep(random.random())
            await bot.channel().send("bati")
            bot.last_bati = time()


bot.run()
