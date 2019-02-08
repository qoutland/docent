from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from itertools import chain
from .forms import SignUpForm
from .models import Profile, Interest, Activity, ActivityType, SavedActivity


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
	
	act_list = []
	i=3
	while len(activity_list) > i:
		act_list.append(activity_list[(i-3):i])
		i+=3
	if len(activity_list) % 3 != 0:
		act_list.append(activity_list[i-3:len(activity_list)])

	context = {
		'activity_list': act_list,
	}

	return render(request, 'index.html', context)

def category(request):
	if request.method == 'GET':
		search_query = request.GET.get('type', None)
		if search_query != None and len(str(search_query)) > 0:
			act_list = []
			try:
				type_id = ActivityType.objects.filter(activity_type=str(search_query))
				type_list = Activity.objects.filter(activity_type=ActivityType.objects.get(activity_type=str(search_query).lower())) #For activity type
			except:
				type_list= []
			activity_list = list(set(act_list) | set(type_list))
		else:
			activity_list = Activity.objects.all()
	
	act_list = []
	i=3
	while len(activity_list) > i:
		act_list.append(activity_list[(i-3):i])
		i+=3
	if len(activity_list) % 3 != 0:
		act_list.append(activity_list[i-3:len(activity_list)])

	context = {
		'activity_list': act_list,
		'type': search_query.capitalize(),
	}

	return render(request, 'category.html', context)


@login_required
def profile(request):
	if request.method == 'GET':
		if request.GET.get('new_interest', None):
			new_interest = request.GET.get('new_interest', None)
			if new_interest != None:
				new_int = ActivityType.objects.all().get(activity_type = new_interest)
				Interest.objects.get_or_create(profile = request.user, act_type = new_int)

	if request.method == 'GET':
		if request.GET.get('old_interest', None):
			rem_interest = request.GET.get('old_interest', None)
			if rem_interest != None:
				Interest.objects.filter(act_type=ActivityType.objects.get(activity_type=rem_interest), profile=request.user.id).delete()

	saved_activity_list = Activity.objects.filter(ID=SavedActivity.objects.get(profile=request.user.id).save_act_id.ID)

	act_list = []
	i=3
	while len(saved_activity_list) > i:
		act_list.append(saved_activity_list[(i-3):i])
		i+=3
	if len(saved_activity_list) % 3 != 0:
		act_list.append(saved_activity_list[i-3:len(saved_activity_list)])

	int_list = ActivityType.objects.all()
	user_interest_list = ActivityType.objects.filter(interest__in=Interest.objects.filter(profile=request.user.pk))
	interest_list = [x for x in int_list if x not in user_interest_list]

	context = {
		'interest_list': interest_list,
		'user_interest_list': user_interest_list,
		'saved_activity_list': act_list,
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

