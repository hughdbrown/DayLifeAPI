# API for looking up news
# Lifted from:
#	http://developer.daylife.com/simple-python-client
# and simplified

class DaylifeAPI(object):
	auth_keys = ['topic_id','article_id','story_id','image_id','quote_id','source_id','set_id','query','name']
	verbs = ['source_getTopics', 'source_getInfo', 'source_getImage', 'source_getArticles',
		'topic_getInfo', 'topic_getTimeLine', 'topic_getRelatedTopics', 'topic_getRelatedStories', 'topic_getRelatedQuotes', 'topic_getRelatedImages', 'topic_getRelatedArticles',
		'search_getRelatedTopics', 'search_getRelatedQuotes','search_getRelatedImages','search_getRelatedArticles', 'search_getQuotesBy','search_getQuotesAbout','search_getMatchingTopics','search_getMatchingSources','search_getCounts',
		'quote_getRelatedTopics', 'quote_getRelatedQuotes', 'quote_getRelatedArticles', 'quote_getInfo',
		'article_getRelatedTopics', 'article_getRelatedQuotes', 'article_getRelatedImages', 'article_getRelatedArticles', 'article_getInfo',]

	def __init__(self, accesskey, sharedsecret, server='freeapi.daylife.com', version='4.4'):
		self.accesskey = accesskey
		self.sharedsecret = sharedsecret
		self.server = server
		self.version = version

	def __getattr__(self, name):
		if not name in DaylifeAPI.verbs:
			raise AttributeError, name
		else:
			def caller(**params):
				url = self.construct_api_url(name, params)
				return self.call_url(url)
			return caller

	def construct_api_url(self, method_name, params):
		params['accesskey'] = self.accesskey
		auth_key, auth_value = self.parse_auth_key(params)
		if not auth_value:
			raise ValueError("No core input could be identified")
		params['signature'] = self.calc_signature(auth_value)
		return 'http://%s/jsonrest/publicapi/%s/%s?%s' % (self.server, self.version, method_name, self.build_query_string(params))

	def build_query_string(self, params):
		from urllib import quote
		iter = params.iteritems
		items = [(k,x) for k,v in iter() if type(v) is list for x in v] + \
				[(k,v) for k,v in iter() if not (type(v) is list)]
		return '&'.join('%s=%s' % (k,quote(str(v))) for k, v in items)

	def call_url(self, url):
		from urllib2 import urlopen
		from simplejson import JSONDecoder
		return JSONDecoder().decode(urlopen(url).read().decode("iso-8859-1"))

	def calc_signature(self, query):
		import md5
		m = md5.new()
		m.update(self.accesskey + self.sharedsecret + query)
		return m.hexdigest()

	def parse_auth_key(self, params):
		values = [(x,params[x]) for x in self.auth_keys if x in params]
		try:
			x, value = values[0]
			if type(value) is list:
				value = ''.join(str(y) for y in sorted(value))
			return (x, value)
		except IndexError:
			return (None,None)
