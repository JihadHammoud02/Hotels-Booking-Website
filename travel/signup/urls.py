from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path

app_name='signup'

urlpatterns = [
    path('',views.create_user,name='create_user'),
]