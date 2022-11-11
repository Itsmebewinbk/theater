from django.shortcuts import render, redirect
from Admin.forms import LogInForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Admin.models import *


def home(request):
    return render(request, "home.html")


def admindashboard(request):
    return render(request, "dashboard.html")


def index(request):
    return render(request, "index.html")


def login_view(request, *args, **kwargs):
    form = LogInForm()
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Login Succesfull")
                if request.user.usertype == 'admin':  # user type
                    return redirect("dashboard")
                elif request.user.usertype == 'customer':
                    return redirect("home")
                elif request.user.usertype == 'theater':
                    return redirect("index")
            else:
                messages.error(request, "invalid username or password")
    return render(request, "login.html", {"form": form})

def user_registration(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "your account has been created")
            return redirect("login")
        else:
            messages.error(request, "registration failed")
            return render(request, "registration.html", {"form": form})
    return render(request, "registration.html", {"form": form})

def logout_view(request):
    logout(request,)
    return redirect("login")