from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django import template
from urllib.parse import urlencode
from itertools import chain
from random import shuffle
from .forms import SignUpForm
from .models import Profile, Interest, Activity, ActivityType, SavedActivity

#Save an activity to a users profile
def saveAct(request):
	if request.method == 'GET':
		save_act = request.GET['post_id'] #Get activity to save or delete
		if save_act: #If there is an activity to save/delete
			if SavedActivity.objects.filter(profile=request.user.id, save_act_id=save_act).exists(): #See if it exists
				SavedActivity.objects.get(profile=request.user.id, save_act_id=save_act).delete() #If it does then delete it
				return HttpResponse("deleted")
			else:
				SavedActivity.objects.get_or_create(profile=request.user, save_act_id=Activity.objects.get(ID=save_act)) #If not create it
				return HttpResponse("created")

#Add or remove an interest from a user profile
def add_removeInterest(request):
	if request.method == 'GET':
		new_interest = request.GET['new_int'] #Get activity to save or delete
		print(new_interest)
		if new_interest: #If there is an activity to save/delete
			print('Checking if it exists')
			if Interest.objects.get(profile=request.user.id, act_type=ActivityType.objects.get(activity_type=new_interest)): #See if it exists
				print('It exists, deleting')
				Interest.objects.get(profile=request.user.id, act_type=ActivityType.objects.get(activity_type=new_interest)).delete() #If it does then delete it
				return HttpResponse("deleted")
			else:
				Interest.objects.get_or_create(profile=request.user, act_type=ActivityType.objects.get(activity_type=new_interest)) #If not create it
				return HttpResponse("created")

#Main page
def index(request):
	if request.method == 'GET': #If the request is a GET method
		search_query = request.GET.get('search_box', None) #Get search box var
		save_act = request.GET.get('save_act', None) #Get activity to save or delete
		category = request.GET.get('category', None) #Get a category type
		sort = request.GET.get('sort', None)
		filter_act = request.GET.get('filter', None)
		if search_query != None: #If there is a search query
			activity_list = getActs(search_query) #Return the results (if there are any)
		else:
			activity_list = Activity.objects.all() #If there was no search_query then return all activities

		if save_act: #If there is an activity to save/delete
			if SavedActivity.objects.filter(profile=request.user.id, save_act_id=save_act).exists(): #See if it exists
				SavedActivity.objects.get(profile=request.user.id, save_act_id=save_act).delete() #If it does then delete it
			else:
				SavedActivity.objects.get_or_create(profile=request.user, save_act_id=Activity.objects.get(ID=save_act)) #If not create it

		if category != None:
			activity_list = getActs(category)
		
		if sort != None:
			if sort == 'az':
				activity_list = activity_list.order_by('name')
			elif sort == 'za':
				activity_list = activity_list.order_by('name').reverse()
			elif sort =='review':
				activity_list = activity_list.filter(origin='y').order_by('avg_review')
			elif sort == 'shuffle':
				activity_list = activity_list.order_by('?')

		if filter_act != None:
			if filter_act == 'yelp':
				activity_list = activity_list.filter(origin='y')
			elif filter_act == 'ticketmaster':
				activity_list = activity_list.filter(origin='t')
			elif filter_act == 'all':
				pass
			
	elif request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('index')

	if request.user.is_authenticated: #If the user is authenticated show them the stars
		saved_list=[] #Create empty list (must do if using the append function)
		if SavedActivity.objects.filter(profile=request.user.id).exists(): #Check if a user has any saved activites
			saved_activity_list = SavedActivity.objects.filter(profile=request.user.id) #Get all of instances (this is not just activities, it includes the user PK as well)
			for save_act in saved_activity_list: #Loop through SavedActivity objects and get the Activity object referenced by its FK
				saved_list.append(Activity.objects.get(ID=save_act.save_act_id.ID)) #Append to the  list
		else:
			saved_list=[] #If the user doesn't have any saved activites return an empty list
	else:
		saved_list=[] #If the user is not authenticated return an empty list
	form = SignUpForm()

	paginator = Paginator(activity_list, 24) # Show 25 contacts per page
	page = request.GET.get('page')
	act_list = paginator.get_page(page)
	result_num = len(activity_list)
	context = {
		'activity_list': act_list,
		'saved_list': saved_list,
		'form': form,
		'search_query': search_query,
		'result_num': result_num,
		'category': category,
		'sort': sort,
		'filter_act': filter_act,
	}
	return render(request, 'index.html', context)

def category(request): #This function is used to present the activities based on the categories (very similiar to search_query) **Maybe can be refactored in the future
	if request.method == 'GET':
		search_query = request.GET.get('type', None)
		activity_list = getActs(search_query)
	if search_query != None:
		search_query= search_query.capitalize()

	form = SignUpForm()

	paginator = Paginator(activity_list, 24) # Show 25 contacts per page
	page = request.GET.get('page')
	act_list = paginator.get_page(page)

	context = {
		'activity_list': act_list,
		'type': search_query,
		'form': form,
	}
	return render(request, 'category.html', context)

@login_required #Can't see this page without loggin in
def profile(request):
	if request.method == 'GET':
		if request.GET.get('new_interest', None): #If user is adding a new interest
			new_interest = request.GET.get('new_interest', None) #Get the var
			new_int = ActivityType.objects.all().get(activity_type = new_interest) #Get the Activity type object
			Interest.objects.get_or_create(profile = request.user, act_type = new_int) #Create a new interest for the user

		if request.GET.get('old_interest', None): #If the user is removing an old interest
			rem_interest = request.GET.get('old_interest', None) #Get the var
			Interest.objects.filter(act_type=ActivityType.objects.get(activity_type=rem_interest), profile=request.user.id).delete() #Delete that object with the user and interest

		if request.GET.get('save_act'): #If the user wants to delete a saved activity from the profile page
			save_act = request.GET.get('save_act', None) #Get the var
			SavedActivity.objects.get(profile=request.user.id, save_act_id=save_act).delete() #Delete that object with user and activity ID

		saved_activity_list = SavedActivity.objects.filter(profile=request.user.id) #Get all Saved Activities in SavedActivities for a specific user
		saved_act_list=[]

		saved_list=[] #Create empty list (must do if using the append function)
		if SavedActivity.objects.filter(profile=request.user.id).exists(): #Check if a user has any saved activites
			saved_activity_list = SavedActivity.objects.filter(profile=request.user.id) #Get all of instances (this is not just activities, it includes the user PK as well)
			for save_act in saved_activity_list: #Loop through SavedActivity objects and get the Activity object referenced by its FK
				saved_list.append(Activity.objects.get(ID=save_act.save_act_id.ID)) #Append to the  list
		else:
			saved_list=[] #If the user doesn't have any saved activites return an empty list
	else:
		saved_list=[] #If the user is not authenticated return an empty list

	int_list = ActivityType.objects.all() #Get all the activity types
	user_interest_list = ActivityType.objects.filter(interest__in=Interest.objects.filter(profile=request.user.pk)) #Get all interests saved by the user
	interest_list = [x for x in int_list if x not in user_interest_list] #Get the rest of the interests

	context = {
		'interest_list': interest_list,
		'user_interest_list': user_interest_list,
		'activity_list': saved_list,
		'saved_list': saved_list,
	}
	return render(request, 'profile.html', context)

#Might be able to delete
def signUp(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = SignUpForm()
	return render(request, 'activity/signup.html', {'form': form})

#Delete sometime
def toTuple(lst):
	act_list = [] #Declare an empty list (Needed for appending)
	i=3 #Set number to create tuples of
	while len(lst) >= i: #While list is 3 or greater (3 or more activites)
		act_list.append(lst[(i-3):i]) #Append an item that is a tuple of 3 ex: ([act1, act2, act3], [act4, act5, act6])
		i+=3 #Increase index by tuple counter
	if len(lst) % 3 != 0: #If there is less than 3 activities in the list or num is not divisible by 3
		act_list.append(lst[i-3:len(lst)]) #Append those items to the list (Might be 1 or 2 empty ones being appened *this doesn't matter)
	return act_list #Return the finished list

def getActs(search_query): #Function that takes in search param and returns activites that match it
	if search_query != None and len(str(search_query)) > 0: #If the search_query is not blank
			act_list = Activity.objects.all().filter(name__contains=str(search_query)) #Get all activities with search_query in the name
			try:
				type_id = ActivityType.objects.filter(activity_type=str(search_query)) #Get activity type with search_query (if exists)
				type_list = Activity.objects.filter(activity_type=ActivityType.objects.get(activity_type=str(search_query).lower())) #Get activities matching the type_id
			except: #If there was no types that matched the search_query
				type_list= []
			activity_list = list(set(act_list) | set(type_list)) #Combine the lists (Name matches and type matches)
			return activity_list #Return the list
	else: #If the search_query was empty
		return [] #Return the empty list