from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

from .models import Profile

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
                
                return redirect('signup')
        else:
            print("password missmatch")
            messages.info(request, 'Password mismatch. Please try again')
            return redirect('signup')

    return render(request, 'signup.html')