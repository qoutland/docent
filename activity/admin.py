from django.contrib import admin
from .models import ActivityType, Activity, Interest, ActivityTypeLine, SavedActivity

admin.site.register(ActivityType)
admin.site.register(Activity)
admin.site.register(Interest)
admin.site.register(ActivityTypeLine)
admin.site.register(SavedActivity)