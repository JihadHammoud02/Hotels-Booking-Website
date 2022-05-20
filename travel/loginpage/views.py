
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, authenticate
# Create your views here.


def check_user(request):  # get data from the html form of the loginpage and verify user credentials from the database
    if request.method == 'POST':  # data retrieve from the html form
        username_client = request.POST.get('username')
        password_client = request.POST.get('pswd')
        user = authenticate(request, username=username_client,
                            password=password_client)  # verification
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('Homepage:hotels_generator'))
        else:
            return render(request, 'loginpage/login.html', {'l': ['error']})
    else:
        return render(request, 'loginpage/login.html')
