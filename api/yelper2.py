#yelp api calls

'''
Search terms: term, location, sort_by, limit, categories, transaction_type(delivery)

https://github.com/gfairchild/yelpapi/blob/master/examples/examples.py
'''

from yelpapi import YelpAPI
from pprint import pprint
import json

def toJSON(result):
    return str(result).replace("'", '"').replace("True",'"TRUE"').replace("False",'"FALSE"').replace("None",'"NULL"')

yelp_api = YelpAPI('0X8SzKkV2v7bo9s_vUvl7IR23KFICRqBaucXJ9DOYQlhgDqXgOeZuzk3ruirXyphW0O6cZXrQfzJRgaHREFQNiBIDXzmwDUvgWdNBQRGLezZ4h7a1D4G8H8Wi-e3W3Yx', timeout_s=3.0)
search_results = yelp_api.search_query(term='music', location='reno, nv', sort_by='rating', limit=25)
pprint(search_results)
pprint(search_results)
print(json.dumps(search_results))
#print(json.dumps(toJSON(search_results), sort_keys=True, indent=4, separators=(',',': ')), file=open("top10.json", "w"))
