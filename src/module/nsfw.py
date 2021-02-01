from .module import IModule
import random
import re
import aiohttp
import json

from discord import Embed

class NSFW(IModule):
  def __init__(self):
    pass

  async def on_message(self, message):
    args = message.clean_content.split()
    if len(args) == 0 or args[0] != "g":
      return

    if args[1] == "e621":
      await self.esix(message)

  async def esix(self, message):
    if not message.channel.is_nsfw():
      await message.channel.send("*Command e621 for NSFW channels only :(*", delete_after=10)
      return
    
    args = message.clean_content.split()
    tags = args[2:-1]
    page_no = args[-1]
    url = "https://e621.net/posts.json?"
    if "page" not in page_no:
      tags.append(page_no)
      page_no = None
    else:
      match = re.search(r'page:(\d+)', page_no)
      page_no = match.group(1)   

    url = url + "tags=" + " ".join(tags)
    if page_no is not None:
      url = url + "&page=" + page_no
    
    post_result = None
    async with aiohttp.ClientSession(headers={"user-agent": "Government(Discord.py) / 0.091 -- https://github.com/jamieboy1337/slutstation; sorry im just lerning :-)"}) as session:
      async with session.get(url) as resp:
        if not (resp.status >= 200 and resp.status < 400):
          print("bad request")
          return
        res = json.loads(await resp.text())['posts']
        post_result = res[random.randint(0, len(res) - 1)]
    
    e = Embed()
    e.title = "e621"
    e.description = f'''by {", ".join(post_result['tags']['artist'])}
Score: {post_result['score']['total']}
{post_result['description']}
**Source (hosted on e621):** {post_result['file']['url']}'''
    e.url = post_result['sample']['url']
    e.set_image(url=post_result['sample']['url'])
    e.set_author(name="e621.net")
    e.color = 0x00549D
    await message.channel.send(embed=e)


    

        
    
