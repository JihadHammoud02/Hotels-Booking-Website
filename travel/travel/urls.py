"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('loginpage.urls')),
    path('signup/',include('signup.urls')),
    path('homepage/',include('Homepage.urls')),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='loginpage/resetpassword.html'),name='password_reset'),
    path('password_reset_sent/',auth_views.PasswordResetDoneView.as_view(template_name='loginpage/password_resent_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='loginpage/password_reset_form.html'),name='password_reset_confirm'),
    path('Password_changed_succesfully/',views.password_reset_complete,name='password_reset_complete')
]


# Url patterns defined to be able to reset password , 