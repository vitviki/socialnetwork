from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        location = request.POST['location']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists. Please try again')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists. Please try again')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()

                user_profile = Profile.objects.create(user=user, id_user=user.id, location=location)
                user_profile.save()
                
                return redirect('signin')
        else:
            messages.info(request, 'Password mismatch. Please try again')
            return redirect('signup')

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or Password is incorrect. Please try again')
            return redirect('signin')
        
    return render(request, 'signin.html')

@login_required(login_url='logout')
def signout(request):
    logout(request)

    return redirect('signin')

