from .module import IModule
import random
import aiohttp
import asyncio

from discord import Embed

import html
import json

class TriviaQuestion:
  __slots__ = ["question", "answers", "correct", "diff", "category"]

  # generates a new question from a single response object
  def __init__(self, q_json):
    self.question = html.unescape(q_json['question'])
    self.category = q_json['category']
    self.diff = q_json['difficulty']
    if q_json['type'] == 'boolean':
      self.answers = []
      # do some setup for booleans
      self.answers.append("True")
      self.answers.append("False")
      if q_json['correct_answer'] == "True":
        self.correct = 0
      else:
        self.correct = 1
    else:   # type is multiple choice
      self.answers = ["" for i in range(4)]
      self.correct = random.randint(0, 3)
      self.answers[self.correct] = html.unescape(q_json['correct_answer'])
      cur = 0
      for i in range(4):
        if i == self.correct:
          continue
        self.answers[i] = html.unescape(q_json['incorrect_answers'][cur])
        cur = cur + 1
  
  def get_embed(self):
    res = Embed()
    res.title = f"{self.category} - {self.diff}"
    res.description = f"*You have 20 seconds to answer the following question.*\n\n"
    if len(self.answers) == 2:
      res.description = res.description + "True or false:\n"
    res.description = res.description + self.question + "\n\n"
    if len(self.answers) > 2:
      a_offset = ord('A')
      for answer in self.answers:
        res.description = res.description + f"{chr(a_offset)}: {answer}\n"
        a_offset = a_offset + 1
    res.color = 0x8050ff
    return res
      


class Trivia(IModule):
  A_EMOJI = 0x0001F1E6
  def __init__(self):
    pass

  
  async def on_message(self, message):
    args = message.clean_content.split()
    if len(args) == 0 or args[0] != "g":
      # no args
      return

    if args[1] == "trivia":
      res = await self.trivia(message)
      reward = f"**The correct answer was {res[1].answers[res[1].correct]}!**\n"
      if len(res[0]) == 0:
        reward = reward + "*No one answered correctly...*"
      else:
        reward += f"*Congratulations to {', '.join([i.name for i in res[0]])} for answering correctly!*"
      await message.channel.send(reward)
      
      
      # list of correct users is below
  async def trivia(self, message):
    q = await self.fetch_trivia()
    r = await message.channel.send(embed=q.get_embed())
    for i in range(len(q.answers)):
      await r.add_reaction(chr(self.A_EMOJI + i))

    await asyncio.sleep(15)
    w = await message.channel.send("***5 seconds remaining!***")
    await asyncio.sleep(5)
    await w.delete()

    correct_users = []
    incorrect_users = []
    r = await message.channel.fetch_message(r.id)
    for reaction in r.reactions:
      offset = ord(str(reaction)[0]) - self.A_EMOJI
      if offset < len(q.answers) and offset >= 0:
        async for user in reaction.users():
          if not user == r.author:
            if offset == q.correct:
              if user not in incorrect_users:
                correct_users.append(user)
            else:
              if user in correct_users:
                correct_users.remove(user)
              incorrect_users.append(user)
    return (correct_users, q)

  async def fetch_trivia(self):
    url = "https://opentdb.com/api.php?amount=1"
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        if not (resp.status >= 200 and resp.status < 400):
          # bad request
          return None
        question = json.loads(await resp.text())['results'][0]
        return TriviaQuestion(question)

        
    pass

