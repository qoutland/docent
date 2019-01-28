from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
	path('signup', views.signUp, name='signup'),
]