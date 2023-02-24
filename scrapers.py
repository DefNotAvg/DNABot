import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from helpers import load_from_json

class Slickdeals:
	def __init__(self, pp=10, sort='newest'):
		'''Initialize Slickdeals class with some attributes.

		Attributes:
			author_name: Author name to appear in Discord embed.
			config: Dictionary containing non-sensitive configuration info.
			deal_score_class: Class within HTML used to identify deal score.
			deal_text: Text within HTML used to identify deal link.
			embed_color: Color of Discord embed sidebar.
			homepage: Slickdeals homepage.
			embed_color: URL of image to use for Discord embed author icon.
			image_property: Property within HTML used to identify deal image.
			pp: Number of results to return per Slickdeals query (max = 100) by default.
			post_class: Class within HTML used to identify post links.
			price_class: Class within HTML used to identify deal price.
			query_link: Link used to query Slickdeals.
			sort: How Slickdeals query results should be sorted (relevance, rating, newest, oldest, last_activity, lowest_price, or highest_price) by default.
		'''
		self.author_name = 'Slickdeals'
		self.config = load_from_json('config.json')
		self.deal_score_class = 'dealScoreBox'
		self.deal_text = 'See Deal'
		self.embed_color = 1339380
		self.homepage = 'https://slickdeals.net'
		self.icon_url = 'https://pbs.twimg.com/profile_images/1567889761729134597/nzAeYF12_400x400.jpg'
		self.image_property = 'og:image'
		self.post_class = 'bp-p-dealLink bp-c-link'
		self.pp = pp
		self.price_class = 'dealPrice'
		self.query_link = 'https://slickdeals.net/newsearch.php'
		self.sort = sort

	async def unaffiliate_link(self, affiliate_link):
		'''Convert Slickdeals affiliate link to an unaffilated link.

		Args:
			affiliate_link: Link to unaffiliate.

		Returns:
			Unaffiliated link string.
		'''
		async with aiohttp.ClientSession(trust_env=True) as session:
			async with session.get(affiliate_link) as response: # Navigate to affiliate link
				return str(response.url).split('?')[0] # Remove tracking params from destination link

	def post_id(self, post_link):
		'''Parse Slickdeals postId from a post link.

		Args:
			post_link: Slickdeals post link.

		Returns:
			PostId string.
		'''
		return post_link.split('/')[-1].split('-')[0]

	def post_title(self, soup):
		'''Parse Slickdeals post title from HTML-parsed Slickdeals post content.

		Args:
			soup: HTML-parsed Slickdeals post content.

		Returns:
			Title string.
		'''
		return soup.title.text.strip()

	def post_price(self, soup):
		'''Parse Slickdeals post price from HTML-parsed Slickdeals post content.

		Args:
			soup: HTML-parsed Slickdeals post content.

		Returns:
			Price float.
		'''
		try:
			return [float(item.text.strip().split('$')[1].split(' ')[0]) for item in soup.find_all('div') if item.get('class') and ' '.join(item.get('class')) == self.price_class][0]
		except IndexError:
			return 0 # Item is free if no HTML object exists with class of price_class

	def post_deal_score(self, soup):
		'''Parse Slickdeals deal score from HTML-parsed Slickdeals post content.

		Args:
			soup: HTML-parsed Slickdeals post content.

		Returns:
			Deal score int.
		'''
		try:
			return [int(item.text) for item in soup.find_all('span') if item.get('class') and ' '.join(item.get('class')) == self.deal_score_class][0]
		except IndexError:
			return None

	async def post_link(self, soup):
		'''Parse Slickdeals post link from HTML-parsed Slickdeals post content.

		Args:
			soup: HTML-parsed Slickdeals post content.

		Returns:
			Link string.
		'''
		try:
			affiliate_link = [item.get('href') for item in soup.find_all('a') if item.text and item.text.strip() == self.deal_text][0]
			return await self.unaffiliate_link(affiliate_link)
		except IndexError:
			return None

	def post_image(self, soup):
		'''Parse Slickdeals post image link from HTML-parsed Slickdeals post content.

		Args:
			soup: HTML-parsed Slickdeals post content.

		Returns:
			Image URL string.
		'''
		try:
			return [item.get('content') for item in soup.find_all('meta') if item.get('property') == self.image_property][0]
		except IndexError:
			return None

	async def post_info(self, post_link):
		'''Gather various post info given a Slickdeals post link.

		Args:
			post_link: Slickdeals post link.

		Returns:
			Dictionary containing various post info.
		'''
		async with aiohttp.ClientSession(trust_env=True) as session:
			async with session.get(post_link) as response:
				soup = BeautifulSoup(await response.text(), 'html.parser')
				return {
					'postId': self.post_id(post_link),
					'title': self.post_title(soup),
					'price': self.post_price(soup),
					'dealScore': self.post_deal_score(soup),
					'link': await self.post_link(soup),
					'image': self.post_image(soup)
				}

	def discord_post_info(self, post_info):
		'''Gather various post info given a Slickdeals post link.

		Args:
			post_info: Dictionary returned by self.post_info().

		Returns:
			Dictionary that can be accepted by discord.py's Embed.from_dict() function.
		'''
		return {
			'title': post_info['title'],
			'url': post_info['link'],
			'color': self.embed_color,
			'timestamp': datetime.utcnow().isoformat(),
			'footer': {
				'icon_url': None if 'footerIcon' not in self.config.keys() else self.config['footerIcon'],
				'text': None if 'footerText' not in self.config.keys() else self.config['footerText']
			},
			'image': {
				'url': post_info['image']
			},
			'author': {
				'name': self.author_name,
				'url': self.homepage,
				'icon_url': self.icon_url
			},
			'fields': [
				{
					'name': 'Price',
					'value': '${:,.2f}'.format(post_info['price']) if post_info['price'] != 0 else 'FREE',
					'inline': True
				},
				{
					'name': 'Deal Score',
					'value': '{}{:,}'.format('+' if post_info['dealScore'] > 0 else '', post_info['dealScore']),
					'inline': True
				}
			]
		}

	async def query_results(self, q, pp=None, sort=None):
		'''Gather Slickdeals query results given a query.

		Args:
			q: Slickdeals search query.
			pp: Results to return (max = 100).
			sort: How results should be sorted (relevance, rating, newest, oldest, last_activity, lowest_price, or highest_price).

		Returns:
			List of dictionaries containing Slickdeals post info.
		'''
		params = (
				('q', q),
				('pp', pp if pp else self.pp),
				('sort', sort if sort else self.sort),
			)
		async with aiohttp.ClientSession(trust_env=True) as session:
			async with session.get(self.query_link, params=params) as response:
				soup = BeautifulSoup(await response.text(), 'html.parser')
				post_links = [self.homepage + item.get('href') for item in soup.find_all('a') if item.get('class') and ' '.join(item.get('class')) == self.post_class and not item.get('href').lower().startswith('http')]
				results = []
				for link in post_links:
					post_info = await self.post_info(link)
					if post_info and all(post_info[key] for key in post_info.keys()):
						results.append(post_info)
				return results