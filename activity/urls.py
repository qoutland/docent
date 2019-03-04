from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
	path('/signup', views.signUp, name='signup'),
    path('category', views.category, name='category'),
    path('save_act/', views.saveAct, name="save_act"),
    path('profile/save_act/', views.saveAct, name="save_act"),
    path('profile/new_interest/', views.add_removeInterest, name="new_interest"),
    ]