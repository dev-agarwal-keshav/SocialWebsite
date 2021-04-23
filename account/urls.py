from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('signup', views.signup, name='Signup'),
    path('login', views.user_login, name='Login'),
    path('logout', views.user_logout, name='Logout'),
]
