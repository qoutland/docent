from django.core.management.base import BaseCommand
from activity.models import Activity, ActivityType, ActivityTypeLine
import json, urllib.request
from pprint import pprint

class Command(BaseCommand):
    args = ''
    help = 'Help string here'

    def _create_activities(self, acts, query_type):
        for act in acts['businesses']:
            activity = Activity(
                name=act['name'],
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
                code=act['location']['zip_code']
            )
            #Check if activity already exists
            if Activity.objects.filter(name=activity.name).count():
                print('Already added')
                #Possible add another typeline here (for duplicate acts)
            else:
                activity.save()
                urllib.request.urlretrieve(act['image_url'],  'activity/static/media/'+ str(activity.ID) + '_pic.jpg')
                activity.pic_url=str(activity.ID) + '_pic.jpg'
                activity.save()
                print('Added activity: ' + str(activity.ID))
                #Check if type exists, if it does then add activity to it | else make that type and create the act type
                if ActivityType.objects.filter(activity_type=query_type).count():
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=query_type), act_id=activity)
                else:
                    ActivityType.objects.create(activity_type=query_type)
                    ActivityTypeLine.objects.create(act_type=ActivityType.objects.get(activity_type=query_type), act_id=activity)
    def toJSON(result):
        return json.loads(str(result).replace("True",'"TRUE"').replace("False",'"FALSE"').replace("None",'"NULL"').replace("'", '"'))

    def _pull_json(self, search_term):
        #yelp_api = YelpAPI('0X8SzKkV2v7bo9s_vUvl7IR23KFICRqBaucXJ9DOYQlhgDqXgOeZuzk3ruirXyphW0O6cZXrQfzJRgaHREFQNiBIDXzmwDUvgWdNBQRGLezZ4h7a1D4G8H8Wi-e3W3Yx', timeout_s=3.0)
        #search_results = yelp_api.search_query(term=search_term, location='reno, nv', sort_by='rating', limit=25)
        #return toJSON(search_results)

        with open('top10.json','r') as f:
            data = json.load(f)
        f.close()
        return data

    def handle(self, *args, **options):
        terms = ['entertainment', 'music', 'food', 'bar', 'sports', 'other']
        for search_term in terms:
            acts = self._pull_json(search_term)
            self._create_activities(acts, search_term)
