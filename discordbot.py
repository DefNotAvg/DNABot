import asyncio
import discord
import pymongo
from helpers import center, smart_time, load_from_json
from scrapers import Slickdeals

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		'''Initialize MyClient class with some additional attributes.

		Attributes:
			config: Dictionary containing non-sensitive configuration info.
			db: Main pymongo database.
		'''
		super().__init__(*args, **kwargs)

		self.config = load_from_json('config.json')
		self.db = pymongo.MongoClient('mongodb://localhost:27017/')['DNABot']

	async def on_ready(self):
		'''Print a message once logged in.'''
		center('[{}] Logged on as {}.'.format(smart_time(), self.user))

	async def setup_hook(self):
		'''Setup loop for self.my_background_task()'''
		self.loop.create_task(self.my_background_task())
	
	async def on_raw_reaction_add(self, payload):
		'''Function to support message forwarding'''
		if payload.user_id != self.user.id and self.config['enableForwarding'] and payload.channel_id == self.config['privateChannelId'] and str(payload.emoji) == '\U0001F4C8':
			for collection in self.db.list_collection_names(): # Iterate through collections to find initial message
				matching_mesage = self.db[collection].find_one({'discordMessages.messageId': payload.message_id})
				if matching_mesage:
					scraper = eval(collection + '()') # Find scraper that matches collection name
					embed = discord.Embed.from_dict(scraper.discord_post_info(matching_mesage)) # Re-create embed
					channel	= self.get_channel(self.config['publicChannelId'])
					message = await channel.send(embed=embed)
					message_info = {
						'messageId': message.id,
						'channelId': message.channel.id
					}
					discord_messages = matching_mesage['discordMessages'] + [message_info]
					self.db[collection].update_one(matching_mesage, {'$set': {'discordMessages': discord_messages}}) # Update stored post info
					break

	async def scrape_slickdeals(self):
		'''Scrape Slickdeals for queries specified within self.config['slickdealsQueries']'''
		print('{}\r'.format(center('[{}] Scraping Slickdeals...'.format(smart_time()), display=False)), end='')
		collection = self.db['Slickdeals']
		scraper = Slickdeals()
		for i in range(len(self.config['slickdealsQueries'])): # Iterate through slickdeals queries
			query = self.config['slickdealsQueries'][i]
			query_results = await scraper.query_results(query) # Get query results
			for k in range(len(query_results)): # Iterate through query results
				post = query_results[k]
				matching_post = collection.find_one({'postId': post['postId']}) # See if post was already shared via Discord
				if not matching_post: # Create new embed
					embed = discord.Embed.from_dict(scraper.discord_post_info(post))
					if self.config['enableForwarding']: # Post to private channel if forwarding is enabled
						channel	= self.get_channel(self.config['privateChannelId'])
					else: # Post to public channel if forwarding is disabled
						channel	= self.get_channel(self.config['publicChannelId'])
					message = await channel.send(embed=embed)
					await message.add_reaction('\U0001F4C8')
					post['discordMessages'] = [
						{
							'messageId': message.id,
							'channelId': message.channel.id
						}
					] # Add message info to post dictionary
					collection.insert_one(post) # Store post info along with message info
				elif any(key not in matching_post.keys() or post[key] != matching_post[key] for key in post.keys()): # Update existing embeds
					embed = discord.Embed.from_dict(scraper.discord_post_info(post))
					for message in matching_post['discordMessages']: # Iterate through prior messages
						channel = self.get_channel(message['channelId'])
						prior_message = await channel.fetch_message(message['messageId'])
						await prior_message.edit(embed=embed) # Update prior message
					collection.update_one(matching_post, {'$set': post}) # Update stored post info
				if k < len(query_results) - 1:
					await asyncio.sleep(3)
			if i < len(self.config['slickdealsQueries']) - 1:
				await asyncio.sleep(60)
		center('[{}] Successfully scraped Slickdeals.'.format(smart_time()))

	async def my_background_task(self):
		'''Process a variety of background tasks.'''
		await self.wait_until_ready()
		await asyncio.sleep(3) # Sleep to allow login message to be sent before proceeding
		while not self.is_closed():
			if 'slickdealsQueries' in self.config.keys():
				await self.scrape_slickdeals()
			await asyncio.sleep(3600)