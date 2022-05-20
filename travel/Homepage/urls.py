from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
app_name='Homepage'

urlpatterns = [
    path('',views.hotels_generator,name='hotels_generator'),
    path('Book_now/<str:id_hotel>/<str:name>/<str:add>/<str:destination>',views.book_now,name='book_now'),
    path('logging_out/',views.log_out,name='logout'),
    path('AboutUs/',views.about_us,name='AboutUs'),
    path('contact/',views.contact_us,name='contact'),
    path('checkout/<str:name>',views.Buy_now,name='checkout')
]
