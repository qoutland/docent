from django.core.management.base import BaseCommand
from activity.models import Activity, ActivityType, ActivityTypeLine
import json, urllib.request, requests, os
from pprint import pprint
from yelpapi import YelpAPI
from PIL import Image
from resizeimage import resizeimage

yelp_api = YelpAPI('0X8SzKkV2v7bo9s_vUvl7IR23KFICRqBaucXJ9DOYQlhgDqXgOeZuzk3ruirXyphW0O6cZXrQfzJRgaHREFQNiBIDXzmwDUvgWdNBQRGLezZ4h7a1D4G8H8Wi-e3W3Yx', timeout_s=3.0)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        #parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--test',
            action='store_true',
            dest='test',
            help='Generate 60 test activities for the application',
        )

    def _create_yelp_activities(self, acts, query_type):
        for act in acts['businesses']:
            activity = Activity(
                name=act['name'],
                avg_review=act['rating'],
                phone_number=act['phone'],
                display_phone=act['display_phone'],
                url=act['url'],
                pic_url=act['image_url'],
                longitude=act['coordinates']['longitude'],
                latitude=act['coordinates']['latitude'],
                address1=act['location']['address1'],
                address2=act['location']['address2'],
                city=act['location']['city'],
                state=act['location']['state'],
                code=act['location']['zip_code'],
                origin='y'
            )
            #Check if activity already exists
            if Activity.objects.filter(name=activity.name).count():
                print('Already added')
                ActivityType.objects.get_or_create(activity_type=query_type)
                if ActivityTypeLine.objects.filter(act_type=ActivityType.objects.get(activity_type=query_type), act_id=Activity.objects.get(name=activity.name)).count():
                    print('Already added type')
                else:
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=query_type), act_id=Activity.objects.get(name=activity.name))
            else:
                activity.save()
                urllib.request.urlretrieve(act['image_url'],  'activity/static/media/'+ str(activity.ID) + '_pic.jpg')
                activity.pic_url=str(activity.ID) + '_pic.jpg'
                with open('activity/static/media/'+ str(activity.ID) + '_pic.jpg', 'r+b') as f:
                    with Image.open(f) as image:
                        cover = resizeimage.resize_cover(image, [286, 197])
                        modal = resizeimage.resize_cover(image, [466, 197])
                        cover.save('activity/static/media/'+ str(activity.ID) + '_pic.jpg', image.format)
                        modal.save('activity/static/media/modal_'+ str(activity.ID) + '_pic.jpg', image.format)
                activity.save()
                print('Added activity: ' + str(activity.ID))
                #Check if type exists, if it does then add activity to it | else make that type and create the act type
                if ActivityType.objects.filter(activity_type=query_type).count():
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=query_type), act_id=activity)
                else:
                    ActivityType.objects.get_or_create(activity_type=query_type)
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=query_type), act_id=activity)

    def _pull_json(self, search_term):
        search_results = yelp_api.search_query(term=search_term, location='reno, nv', sort_by='rating', limit=25)
        print('returning api results: ' + search_term)
        return json.loads(json.dumps(search_results))

    def _test_yelp_data(self, query_type):
        with open('top10.json','r') as f:
            acts = json.load(f)
        f.close()
        for act in acts['businesses']:
            activity = Activity(
                name=act['name'],
                avg_review=act['rating'],
                phone_number=act['phone'],
                display_phone=act['display_phone'],
                url=act['url'],
                pic_url=act['image_url'],
                longitude=act['coordinates']['longitude'],
                latitude=act['coordinates']['latitude'],
                address1=act['location']['address1'],
                address2=act['location']['address2'],
                city=act['location']['city'],
                state=act['location']['state'],
                code=act['location']['zip_code'],
                origin='y'
            )
            activity.save()
            urllib.request.urlretrieve(act['image_url'],  'activity/static/media/'+ str(activity.ID) + '_pic.jpg')
            activity.pic_url=str(activity.ID) + '_pic.jpg'
            with open('activity/static/media/'+ str(activity.ID) + '_pic.jpg', 'r+b') as f:
                    with Image.open(f) as image:
                        cover = resizeimage.resize_cover(image, [286, 197])
                        modal = resizeimage.resize_cover(image, [466, 197])
                        cover.save('activity/static/media/'+ str(activity.ID) + '_pic.jpg', image.format)
                        modal.save('activity/static/media/modal_'+ str(activity.ID) + '_pic.jpg', image.format)
            activity.save()
            print('Added activity: ' + str(activity.ID))
            #Check if type exists, if it does then add activity to it | else make that type and create the act type
            if ActivityType.objects.filter(activity_type=query_type).count():
                ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=query_type), act_id=activity)
            else:
                ActivityType.objects.get_or_create(activity_type=query_type)
                ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=query_type), act_id=activity)

    def _test_ticket_data(self):
        with open('events.json','r') as f:
            data = json.load(f)
        f.close()
        events = data['_embedded']['events']
        for e in events:
            activity = Activity(
                name=e['name'],
                url=e['url'],
                event_date=e['dates']['start']['localDate'],
                pic_url=e['images'][2]['url'],
                city=e['_embedded']['venues'][0]['city']['name'],
                state=e['_embedded']['venues'][0]['state']['stateCode'],
                code=e['_embedded']['venues'][0]['postalCode'],
                longitude=e['_embedded']['venues'][0]['location']['longitude'],
                latitude=e['_embedded']['venues'][0]['location']['latitude'],
                address1=e['_embedded']['venues'][0]['address']['line1'],
                origin='t'
            )
            if Activity.objects.filter(name=activity.name).count():
                print('Already added')
                ActivityType.objects.get_or_create(activity_type=e['classifications'][0]['segment']['name'].lower())

                if ActivityTypeLine.objects.filter(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=Activity.objects.get(name=activity.name)).count():
                    print('Already added type')
                else:
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=Activity.objects.get(name=activity.name))
            else:
                activity.save()
                x=1
                i=0
                while x==1:
                    if e['images'][i]['width'] >= 466 and e['images'][i]['height'] >= 197:
                        urllib.request.urlretrieve(e['images'][i]['url'],  'activity/static/media/'+ str(activity.ID) + '_pic.jpg')
                        x=0
                    else:
                        i+=1
                activity.pic_url=str(activity.ID) + '_pic.jpg'
                with open('activity/static/media/'+ str(activity.ID) + '_pic.jpg', 'r+b') as f:
                    with Image.open(f) as image:
                        cover = resizeimage.resize_cover(image, [286, 197])
                        modal = resizeimage.resize_cover(image, [466, 197])
                        cover.save('activity/static/media/'+ str(activity.ID) + '_pic.jpg', image.format)
                        modal.save('activity/static/media/modal_'+ str(activity.ID) + '_pic.jpg', image.format)
                activity.save()
                print('Added activity: ' + str(activity.ID))
                #Check if type exists, if it does then add activity to it | else make that type and create the act type
                if ActivityType.objects.filter(activity_type=e['classifications'][0]['segment']['name']).count():
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=activity)
                else:
                    ActivityType.objects.get_or_create(activity_type=e['classifications'][0]['segment']['name'].lower())
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=activity)

    def _create_ticketmaster_activities(self):
        data = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?stateCode=NV&city=Reno&size=100&apikey=RvKwUT6q6DuDH6eBGG8zARBNdI394ZIa').json()
        events = data['_embedded']['events']
        for e in events:
            activity = Activity(
                name=e['name'],
                url=e['url'],
                event_date=e['dates']['start']['localDate'],
                pic_url=e['images'][2]['url'],
                city=e['_embedded']['venues'][0]['city']['name'],
                state=e['_embedded']['venues'][0]['state']['stateCode'],
                code=e['_embedded']['venues'][0]['postalCode'],
                longitude=e['_embedded']['venues'][0]['location']['longitude'],
                latitude=e['_embedded']['venues'][0]['location']['latitude'],
                address1=e['_embedded']['venues'][0]['address']['line1'],
                origin='t'
            )
            if Activity.objects.filter(name=activity.name).count():
                print('Already added')
                if ActivityTypeLine.objects.filter(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=Activity.objects.get(name=activity.name)).count():
                    print('Already added type')
                else:
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=Activity.objects.get(name=activity.name))
            else:
                activity.save()
                x=1
                i=0
                while x==1:
                    if e['images'][i]['width'] >= 466 and e['images'][i]['height'] >= 197:
                        urllib.request.urlretrieve(e['images'][i]['url'],  'activity/static/media/'+ str(activity.ID) + '_pic.jpg')
                        x=0
                    else:
                        i+=1
                activity.pic_url=str(activity.ID) + '_pic.jpg'
                with open('activity/static/media/'+ str(activity.ID) + '_pic.jpg', 'r+b') as f:
                    with Image.open(f) as image:
                        cover = resizeimage.resize_cover(image, [286, 197])
                        modal = resizeimage.resize_cover(image, [466, 197])
                        cover.save('activity/static/media/'+ str(activity.ID) + '_pic.jpg', image.format)
                        modal.save('activity/static/media/modal_'+ str(activity.ID) + '_pic.jpg', image.format)
                activity.save()
                print('Added activity: ' + str(activity.ID))
                #Check if type exists, if it does then add activity to it | else make that type and create the act type
                if ActivityType.objects.filter(activity_type=e['classifications'][0]['segment']['name']).count():
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=activity)
                else:
                    ActivityType.objects.get_or_create(activity_type=e['classifications'][0]['segment']['name'].lower())
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=e['classifications'][0]['segment']['name'].lower()), act_id=activity)

    def _create_hiking_activities(self):
        data = requests.get('https://www.hikingproject.com/data/get-trails?lat=39.5296&lon=-119.8138&maxResults=50&key=200446744-75b255e6be35c19e68574645f0e16570').json()
        trails = data['trails']
        for trail in trails:
            activity = Activity(
                name=trail['name'],
                url=trail['url'],
                pic_url=trail['imgMedium'],
                avg_review=trail['stars'],
                longitude=trail['longitude'],
                latitude=trail['latitude'],
                description=trail['summary'],
                length=trail['length'],
                origin='h'
            )
            if Activity.objects.filter(name=activity.name).count():
                print('Already added')
                if ActivityType.objects.filter(activity_type=trail['type'].lower()).count():
                    if ActivityTypeLine.objects.filter(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=Activity.objects.get(name=activity.name)).count():
                        print('Already added type')
                    else:
                        ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=Activity.objects.get(name=activity.name))
                else:
                    ActivityType.objects.create(activity_type=trail['type'].lower())
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=Activity.objects.get(name=activity.name))
            else:
                activity.save()
                if trail['imgMedium'] != '':
                    urllib.request.urlretrieve(trail['imgMedium'],  'activity/static/media/'+ str(activity.ID) + '_pic.jpg')             
                    activity.pic_url=str(activity.ID) + '_pic.jpg'
                    with open('activity/static/media/'+ str(activity.ID) + '_pic.jpg', 'r+b') as f:
                        with Image.open(f) as image:
                            cover = resizeimage.resize_cover(image, [286, 197])
                            modal = resizeimage.resize_cover(image, [466, 197])
                            cover.save('activity/static/media/'+ str(activity.ID) + '_pic.jpg', image.format)
                            modal.save('activity/static/media/modal_'+ str(activity.ID) + '_pic.jpg', image.format)
                    activity.save()
                print('Added activity: ' + str(activity.ID))
                #Check if type exists, if it does then add activity to it | else make that type and create the act type
                if ActivityType.objects.filter(activity_type=trail['type']).count():
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=activity)
                else:
                    ActivityType.objects.get_or_create(activity_type=trail['type'].lower())
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=activity)

    def _test_hike_data(self):
        with open('hikes.json','r') as f:
            data = json.load(f)
        f.close()
        trails = data['trails']
        for trail in trails:
            activity = Activity(
                name=trail['name'],
                url=trail['url'],
                pic_url=trail['imgMedium'],
                avg_review=trail['stars'],
                longitude=trail['longitude'],
                latitude=trail['latitude'],
                description=trail['summary'],
                length=trail['length'],
                origin='h'
            )
            if Activity.objects.filter(name=activity.name).count():
                print('Already added')
                if ActivityType.objects.filter(activity_type=trail['type'].lower()).count():
                    if ActivityTypeLine.objects.filter(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=Activity.objects.get(name=activity.name)).count():
                        print('Already added type')
                    else:
                        ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=Activity.objects.get(name=activity.name))
                else:
                    ActivityType.objects.create(activity_type=trail['type'].lower())
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=Activity.objects.get(name=activity.name))
            else:
                activity.save()
                if trail['imgMedium'] != '':
                    urllib.request.urlretrieve(trail['imgMedium'],  'activity/static/media/'+ str(activity.ID) + '_pic.jpg')             
                    activity.pic_url=str(activity.ID) + '_pic.jpg'
                    with open('activity/static/media/'+ str(activity.ID) + '_pic.jpg', 'r+b') as f:
                        with Image.open(f) as image:
                            cover = resizeimage.resize_cover(image, [286, 197])
                            modal = resizeimage.resize_cover(image, [466, 197])
                            cover.save('activity/static/media/'+ str(activity.ID) + '_pic.jpg', image.format)
                            modal.save('activity/static/media/modal_'+ str(activity.ID) + '_pic.jpg', image.format)
                    activity.save()
                print('Added activity: ' + str(activity.ID))
                #Check if type exists, if it does then add activity to it | else make that type and create the act type
                if ActivityType.objects.filter(activity_type=trail['type']).count():
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=activity)
                else:
                    ActivityType.objects.get_or_create(activity_type=trail['type'].lower())
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=trail['type'].lower()), act_id=activity)

    def handle(self, *args, **options):
        terms = ['entertainment', 'music', 'food', 'bar', 'sports', 'other']
        if not os.path.exists('activity/static/media'):
            os.makedirs('activity/static/media')
        if options['test']:
            for search_term in terms:
                self._test_yelp_data(search_term)
                self._test_ticket_data()
                self._test_hike_data()
                
        else:
            for search_term in terms:
                acts = self._pull_json(search_term)
                self._create_yelp_activities(acts, search_term)
            self._create_ticketmaster_activities()
            self._create_hiking_activities()
