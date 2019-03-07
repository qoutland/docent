import json
from pprint import pprint
from activity.models import Activity
with open('top10.json','r') as f:
    data = json.load(f)

for act in data['businesses']:
    Activity.objects.create(
        name=act['name'],
        phone_number=act['phone'],
        display_phone=act['display_phone'],
        url=act['url'],
        pic_url=act['image_url'],
        longitude=act['location']['longitude'],
        latitude=act['location']['latitude'],
        address1=act['location']['address1'],
        address2=act['location']['address2'],
        city=act['location']['city'],
        state=act['location']['state'],
        code=act['location']['zip_code']
    )

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
