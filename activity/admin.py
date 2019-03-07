from django.contrib import admin
from .models import ActivityType, Activity, Interest, ActivityTypeLine, SavedActivity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'ID',
        'name',
    )

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = (
        'type_id',
        'activity_type'

    )

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'act_type'
    )

@admin.register(ActivityTypeLine)
class ActivityTypeLineAdmin(admin.ModelAdmin):
    list_display = (
        'act_type',
        'act_id'
    )

@admin.register(SavedActivity)
class SavedActivityAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'save_act_id'
    )