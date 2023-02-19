import discord
from helpers import center, smart_time

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	async def on_ready(self):
		center('[{}] Logged on as {}'.format(smart_time(), self.user))
	
	async def on_raw_reaction_add(self, payload):
		pass

	async def on_message(self, message):
		pass

	async def my_background_task(self):
		pass