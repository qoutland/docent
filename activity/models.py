from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField

class Profile(models.Model): #Don't know if this is needed anymore
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	
class ActivityType(models.Model): #Activity Typing
	type_id = models.AutoField(primary_key=True) #A primary key to keep track of IDs
	activity_type = models.CharField(null=False, blank=False, max_length=20) #The description of the key

class Interest(models.Model): #An entry for a user and an ActivityType
	profile = models.ForeignKey(User, on_delete=models.CASCADE)
	act_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)

class Activity(models.Model): #An activity object (using a PK for individual references)
	ID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=250)
	activity_type = models.ManyToManyField(ActivityType, through='ActivityTypeLine')
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	display_phone = models.CharField(blank=True, max_length=17)
	url = models.URLField(blank=True)
	pic_url = models.CharField(blank=True, max_length=20)
	longitude = models.FloatField(null=True)
	latitude = models.FloatField(null=True)
	address1 = models.CharField(_("address"), max_length=128, null=True,)
	address2 = models.CharField(_("address cont'd"), max_length=128, null=True)
	city = models.CharField(_("city"), max_length=64, default="Reno")
	state = USStateField(_("state"), default="NV")
	code = models.CharField(_("zip code"), max_length=5, null=True)
	description = models.TextField(blank=True, max_length=300)
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)

class ActivityTypeLine(models.Model): #Allows activities to have multiple types
	act_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
	act_id = models.ForeignKey(Activity, on_delete=models.CASCADE)

class SavedActivity(models.Model): #Allows users to be able to save multiple activites 
	profile = models.ForeignKey(User, on_delete=models.CASCADE)
	save_act_id = models.ForeignKey(Activity, on_delete=models.CASCADE)