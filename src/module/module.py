# basic interface for a module
# modules should just have functions corresponding with desired behavior

import asyncio

class IModule:
  async def on_message(self, message):
    raise NotImplementedError()
 
