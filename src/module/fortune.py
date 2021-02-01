from .module import IModule
import random
import time
from datetime import datetime
from discord import Embed

# tba
# there's definitely some way to bind a coroutine
# by using a sync function to schedule an async task

class Fortune(IModule):
  __slots__ = ["fortunes"]
  FORTUNE_FILE = "resources/fortune_cookie.txt"
  def __init__(self):
    self.fortunes = []
    self.methods = {}
    with open(self.FORTUNE_FILE, "r") as fortune_file:
      line = fortune_file.readline().rstrip("\n")
      while line != "":
        print(line)
        self.fortunes.append(line)
        line = fortune_file.readline().rstrip()

  async def on_message(self, message):
    args = message.clean_content.split()
    if len(args) == 0 or args[0] != "g":
      # no args
      return
    if args[1] == "fortune":
      await self.fortune(message)
    

  
  async def fortune(self, message):
    # use user and time to generate a fortune
    user_hash = hash(message.author.name)

    d1 = datetime.now()
    d0 = datetime(2000, 1, 1);
    days = (d1 - d0).days;

    user_hash = user_hash ^ days
    cur_date = d1.strftime("%B %d, %Y")

    random.seed(user_hash)
    fortune_ord = random.randint(0, len(self.fortunes) - 1)
    result = Embed()
    result.title = f"{message.author.nick}'s fortune for {cur_date}..."
    result.color = 0xE8522E
    result.description = f"*{self.fortunes[fortune_ord]}*"

    await message.channel.send(embed=result)
