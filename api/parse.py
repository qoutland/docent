import json
from pprint import pprint

with open('top10.json','r') as f:
    data = json.load(f)

for act in data['businesses']:
    print(act['name'])
    #print(act['coordinates']['latitude'])
    #print(act['coordinates']['longitude'])
    #print(act['location']['address1'])
    #print(act['location']['address2'])
    #print(act['location']['city'])
    #print(act['location']['display_address'])
    #print(act['display_phone'])
    #print(act['phone'])
    #print(act['image_url'])
    #print(act['url'])
