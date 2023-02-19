import os
from discord import Intents
from logging import WARNING
from discordbot import MyClient
from helpers import header, center, smart_time

if __name__ == '__main__':
	header()
	token = os.getenv('discordToken')
	if token:
		intents = Intents.all()
		client = MyClient(intents=intents)
		client.run(token, log_level=WARNING)
	else:
		center('[{}] Please set environment variable, discordToken, before proceeding.'.format(smart_time()))