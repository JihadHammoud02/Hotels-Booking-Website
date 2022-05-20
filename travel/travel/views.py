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
def password_reset_complete(request):
    return HttpResponseRedirect(reverse('loginpage:check_user'))