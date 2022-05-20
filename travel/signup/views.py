import email
from django.shortcuts import render
from django.contrib.auth.models import User
from re import template

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext, loader
from django.urls import reverse
from django.contrib.auth import login,authenticate
import loginpage
from django.contrib import messages

# Create your views here.

def create_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email_client=request.POST.get('email')
        password=request.POST.get('pswd')
        conf_pass=request.POST.get('pswdd')
        all_users=User.objects.all()
        list_of_emails=[]
        for mail in all_users:
            list_of_emails.append(mail.email)
        if email_client in list_of_emails:
            return render(request,'signup/signupform.html',{'l4':['error']}) # email already in use
        if conf_pass!=password:
            return render(request,'signup/signupform.html',{'l3':['error']}) # passwords don't match


        user = User.objects.create_user(username,email_client,password)
        user.first_name=request.POST.get('firstname')
        user.last_name=request.POST.get('familyname')
        user.save()
        return HttpResponseRedirect(reverse('loginpage:check_user'))    #user creation successful --> redirects to login page
    else:
        return render(request,'signup/signupform.html')