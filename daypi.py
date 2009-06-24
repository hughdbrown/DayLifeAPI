from DayLifeAPI import *
import time
from pprint import pprint

def test_daylifeapi(**params):
	args = {"accesskey":"8befa1cf0a7c0291613242235638a662", "sharedsecret":"2e548ef751397c653752057adcff0c9f"}
	api = DaylifeAPI(**args)
	ret = api.search_getRelatedArticles(**params)
	print pprint(ret)

if __name__ == "__main__":
	#getting articles related to jesus in the last 7 days sorted by date
	now = long(time.time())
	weekago = now - (7*86400)
	test_daylifeapi(query="jesus", start_time=weekago, end_time=now, sort="date")
