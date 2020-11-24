import json
import os
from datetime import datetime

from twitchio.ext import commands


@commands.core.cog(name="KaputtCog")
class KaputtCog:
    def __init__(self, bot):
        self.bot = bot
        self.kaputt_file = os.getenv("KAPUTT_FILE")
        self.kaputt = {}
        self.load_kaputt()

    def load_kaputt(self):
        kaputt_file = open(self.kaputt_file, mode='r')
        self.kaputt = json.load(kaputt_file)

    def save_kaputt(self):
        kaputt_file = open(self.kaputt_file, mode='w')
        json.dump(self.kaputt, kaputt_file)

    @commands.command(name="kaputt")
    async def cmd_kaputt(self, ctx, name, *args):
        today = datetime.now().strftime("%Y-%m-%d")
        name = name.lower()
        add = True if (len(args) > 0 and args[0] == "+") else False

        if self.kaputt["stream_date"] != today:
            self.kaputt["stream_date"] = today

            for name in self.kaputt["streamer"].values():
                name[0] = 0

        if not self.kaputt["streamer"].get(name):
            if add:
                self.kaputt["streamer"][name] = [0, 0]
            else:
                return

        count = self.kaputt["streamer"][name]
        count[0] = count[0] + 1
        count[1] = count[1] + 1
        await ctx.send(
            f'{name.capitalize()} hat heute schon {self.kaputt["streamer"][name][0]} mal das Projekt kaputt gemacht! '
            f'Insgesamt sogar schon mindestens {self.kaputt["streamer"][name][1]} mal!!! So klappt es nicht!')

        self.save_kaputt()
