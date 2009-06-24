from urllib import urlencode, quote
from urllib2 import urlopen
import md5, types
import simplejson

class DaylifeAPI(object):

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
				#print url
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
		iter = params.iteritems
		items = [(k,x) for k,v in iter() if type(v) is types.ListType for x in v] + \
				[(k,v) for k,v in iter() if not (type(v) is types.ListType)]
		return '&'.join('%s=%s'%(k,quote(str(v))) for k, v in items)

	def call_url(self, url):
		#print str(url)
		x = urlopen(url)
		js = simplejson.JSONDecoder()
		return js.decode(x.read().decode("iso-8859-1"))

	def calc_signature(self, query):
		m = md5.new()
		m.update(self.accesskey + self.sharedsecret + query)
		return m.hexdigest()

	def parse_auth_key(self, params):
		keys = [x for x in self.auth_keys if x in params]
		if len(keys):
			value = params[keys[0]]
			if type(value) is types.ListType:
				value = ''.join(str(x) for x in sorted(value))
			print value
			return (x, value)
		else:
			return (None,None)

def test_daylifeapi():
	import time
	from pprint import pprint
	api = DaylifeAPI("8befa1cf0a7c0291613242235638a662",
					 "2e548ef751397c653752057adcff0c9f",
					 "freeapi.daylife.com")

	#getting articles related to jesus in the last 7 days sorted by date
	ret = api.search_getRelatedArticles(query='jesus',
										start_time=long(time.time() - (7*86400)),
										end_time=long(time.time()),
										sort="date")
	print pprint(ret)
	
if __name__ == "__main__":
	test_daylifeapi()

