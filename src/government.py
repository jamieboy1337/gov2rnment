# files will be registered by the client
# use a basic interface to organize them
import discord
import asyncio
from module.trivia import Trivia
from module.fortune import Fortune
from module.nsfw import NSFW

class Government(discord.Client):
  __slots__ = ["modules"]
  def __init__(self):
    super().__init__()
    self.modules = []
  

  def add_module(self, module):
    self.modules.append(module)

  async def on_message(self, message):
    if message.author.bot:
      return

    print(f"{message.author.name}: {message.clean_content}")

    # check the contents of the message
    # probably do nothing right now
    # pass it to the modules right away

    for module in self.modules:
      await module.on_message(message)


if __name__ == '__main__':
  client = Government()
  trivia = Trivia()
  fortune = Fortune()
  nsfw = NSFW()
  client.add_module(trivia)
  client.add_module(fortune)
  client.add_module(nsfw)

  token = ""
  with open("resources/discord_token.txt", "r") as tokenfile:
    token = tokenfile.readline().rstrip()
  client.run(token)
    