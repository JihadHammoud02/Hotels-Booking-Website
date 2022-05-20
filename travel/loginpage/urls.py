from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
app_name='loginpage'
urlpatterns = [
    path('',views.check_user,name='check_user'),
    
]
