import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docent.settings')
from activity.models import Profile, Activity, ActivityType, Interest


def populate():
    #add_profile()
    add_activity_type(description='movie')
    add_activity_type(description='golf')
    add_activity_type(description='sports')
    add_activity_type(description='restaurant')

    add_activity(name='Century Movie Theaters',
    activity_type=ActivityType.objects.all().get(name='movie'),
    phone_number='7751234567',
    url='https://movietheater.com',
    open_hour='06:00:00',
    close_hour='00:00:00',
    description='Come watch the latest movies in our lush theaters',
    address_1='123 Movie Drive',
    address_2='',
    city='Reno',
    state='Nevada',
    code='89502')

    add_activity(name='Golf Course',
    activity_type=ActivityType.objects.all().get(name='golf'),
    phone_number='7751236548',
    url='https://golfing.com',
    open_hour='06:00:00',
    close_hour='06:00:00',
    description='Play a round at our links',
    address_1='123 Golf Street',
    address_2='',
    city='Reno',
    state='Nevada',
    code='89502')

    add_activity(name='Mexican Cantina',
    activity_type=ActivityType.objects.all().get(name='restaurant'),
    phone_number='7751238975',
    url='https://thecantina.com',
    open_hour='10:00:00',
    close_hour='22:00:00',
    description='Enjoy tacos, burritos, and much more!',
    address_1='123 Cantina Road',
    address_2='',
    city='Reno',
    state='Nevada',
    code='89502')

    add_activity(name='Century Movie Theaters',
    activity_type=ActivityType.objects.all().get(name='movie'),
    phone_number='7751234567',
    url='https://movietheater.com',
    open_hour='06:00:00',
    close_hour='00:00:00',
    description='Come watch the latest movies in our lush theaters',
    address_1='123 Movie Drive',
    address_2='',
    city='Reno',
    state='Nevada',
    code='89502')



def add_profile(user, birthday):
    p = Profile.objects.get_or_create(user=user, birthday=birthday)
    return p

def add_activity_type(description):
    a = ActivityType.objects.get_or_create(description=description)
    return a

def add_activity(name, activity_type, phone_number, url, open_hour, close_hour, description, address_1, address_2, city, state, code):
    A = Activity.objects.get_or_create(name=name, activity_type=activity_type, phone_number=phone_number, url=url, open_hour=open_hour, close_hour=close_hour, description=description, address_1=address_1, address_2=address_2, city=city, state=state, code=code)
    return A

def add_interest(user, activity_type):
    i = Interest.objects.get_or_create(user=user, activity_type=activity_type)
    return i

def main():
    print("Starting Database population script...")
    populate()

# Start execution here!
if __name__ == '__main__':
    main()