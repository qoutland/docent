from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	birthday = models.DateField(null=True, blank=False)
	
	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
		   Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

class ActivityType(models.Model):
	type_id = models.AutoField(primary_key=True)
	activity_type = models.CharField(null=False, blank=False, max_length=20)

class Interest(models.Model):
	profile = models.ForeignKey(User, on_delete=models.CASCADE)
	act_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)

class Activity(models.Model):
	ID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=250)
	activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	url = models.URLField(blank=True)
	open_hour = models.TimeField()
	close_hour = models.TimeField()
	description = models.TextField(blank=True, max_length=300)
	address_1 = models.CharField(_("address"), max_length=128, null=True,)
	address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True)
	city = models.CharField(_("city"), max_length=64, default="Reno")
	state = USStateField(_("state"), default="NV")
	code = models.CharField(_("zip code"), max_length=5, null=True)



	
#class Review(models.Model):