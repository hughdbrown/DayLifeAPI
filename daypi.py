from urllib import urlencode, quote
from urllib2 import urlopen
import md5, types
#import cjson
import simplejson

class DaylifeAPI:

	auth_keys = ['topic_id',
				 'article_id',
				 'story_id',
				 'image_id',
				 'quote_id',
				 'source_id',
				 'set_id',
				 'query',
				 'name'
				 ]

	def __init__(self, accesskey, sharedsecret, server='freeapi.daylife.com', version='4.2'):
		self.accesskey = accesskey
		self.sharedsecret = sharedsecret
		self.server = server
		self.version = version

	def __getattr__(self, name):
		if name.startswith('_'):
			raise AttributeError, name
		else:
			def caller(**params):
				url = self.construct_api_url(name, params)
				print url
				return self.call_url(url)
			return caller
			
	def construct_api_url(self, method_name, params):
		params['accesskey'] = self.accesskey
		auth_key, auth_value = self.parse_auth_key(params)
		if not auth_value:
			raise ValueError("No core input could be identified")
		params['signature'] = self.calc_signature(auth_value)
		url = 'http://' \
					+ str(self.server) \
					+ '/jsonrest/publicapi/' \
					+ str(self.version) \
					+ '/' + method_name \
					+ '?' \
					+ self.build_query_string(params)
		return url

	def build_query_string(self, params):
		qlist = []
		for k,v in params.iteritems():
			if type(v) is types.ListType:
				# list of ids
				qlist.extend( ['%s=%s'%(k,quote(str(x))) for x in v] )
			else:
				# keys don't need quoting
				qlist.append('%s=%s'%(k,quote(str(v))))    
		return '&'.join(qlist)

	def call_url(self, url):
		print str(url)
		x = urlopen(url)
		#return cjson.decode(x.read())
		js = simplejson.JSONDecoder()
		return js.decode(x.read())
		

	def calc_signature(self, query):
		m = md5.new()
		m.update(self.accesskey)
		m.update(self.sharedsecret)
		m.update(query)
		return m.hexdigest()

	def parse_auth_key(self, params):
		for x in self.auth_keys:
			if x in params:
				value = params[x]
				if type(value) is types.ListType:
					value = value[:]
					value.sort()
					value_str = ''
					for x in value:
						value_str = value_str + str(x)
					value = value_str
				print value
				return (x, value)
		return (None,None)


def test_daylifeapi():
	import time
	from pprint import pprint
	api = DaylifeAPI("8befa1cf0a7c0291613242235638a662",
					 "2e548ef751397c653752057adcff0c9f",
					 "freeapi.daylife.com")

	#getting articles related to jeses in the last 7 days sorted by date
	ret = api.search_getRelatedArticles(query='jesus',
										start_time=long(time.time() - (7*86400)),
										end_time=long(time.time()),
										sort="date")
	print pprint(ret)
	
if __name__ == "__main__":
	test_daylifeapi()

