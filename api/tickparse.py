import json



with open('events.json', 'r') as f:
    data = json.load(f)
f.close()
events = data['_embedded']['events']
for e in events:
    print('Name: ' + e['name'])
    print('URL: ' + e['url'])
    print('PicURL: ' + e['images'][1]['url'])
    try:
        print('Start Date: ' + e['dates']['start']['dateTime'])
    except KeyError:
                print('Start Date: Not announced')
    print('Activity Type: ' + e['classifications'][0]['segment']['name'])
    e_addr = e['_embedded']['venues'][0]
    print('City: ' + e_addr['city']['name'])
    print('State: ' + e_addr['state']['stateCode'])
    print('Code: ' + e_addr['postalCode'])
    print('Address: ' + e_addr['address']['line1'])
    print('Longitude: ' + e_addr['location']['longitude'])
    print('Latitude: ' + e_addr['location']['latitude'])
    print()
