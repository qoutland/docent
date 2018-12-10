from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic

from itertools import chain

from .forms import SignUpForm

from .models import Profile, Interest, Activity, ActivityType

def index(request):

	if request.method == 'GET':
		search_query = request.GET.get('search_box', None)
		if search_query != None and len(str(search_query)) > 0:
			act_list = Activity.objects.all().filter(name__contains=str(search_query))
			try:
				type_id = ActivityType.objects.filter(activity_type=str(search_query))
				type_list = Activity.objects.filter(activity_type=ActivityType.objects.get(activity_type=str(search_query).lower())) #For activity type
			except:
				type_list= []
			activity_list = list(set(act_list) | set(type_list))
		else:
			activity_list = Activity.objects.all()
	
	num_profiles = Profile.objects.all().count()
	num_activities = Activity.objects.all().count()
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits+1

	context = {
		'activity_list': activity_list,
		'num_activities': num_activities,
		'num_visits': num_visits,
		'num_profiles': num_profiles,
	}

	return render(request, 'index.html', context)
	
def profile(request):
	if request.method == 'GET':
		new_interest = request.GET.get('new_interest', None)
		if new_interest != None:
			new_int = ActivityType.objects.all().get(activity_type = new_interest)
			Interest.objects.get_or_create(profile = request.user, act_type = new_int)

	int_list = ActivityType.objects.all()
	user_interest_list = ActivityType.objects.filter(interest__in=Interest.objects.filter(profile=request.user.pk))
	interest_list = [x for x in int_list if x not in user_interest_list]

	context = {
		'interest_list': interest_list,
		'user_interest_list': user_interest_list,
	}

	return render(request, 'activity/profile.html', context)

def signUp(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.birthday = form.cleaned_data.get('birthday')
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = SignUpForm()
	return render(request, 'activity/signup.html', {'form': form})