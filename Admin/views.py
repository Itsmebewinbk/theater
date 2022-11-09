from django.shortcuts import render, redirect
from Admin.forms import LogInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Admin.models import *

def index(request):
    return render(request,"home.html")
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
                if request.user.usertype=="admin":#user type
                    redirect("dashboard")
                elif request.user.usertype=='customer':
                    redirect("home")
                if request.user.usertype=='theater':
                    redirect("index")
            else:
                messages.error(request, "invalid username or password")
    return render(request, "login.html", {"form": form})

