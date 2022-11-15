from django.shortcuts import render, redirect
from Admin.forms import LogInForm, RegistrationForm
from Admin.forms import AdminTheatreRegistrationForm
from Theater.models import Theater,Screen,Movie,Show
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Admin.decorators import signin_required
from Admin.models import *

@signin_required
def home(request):
    return render(request, "home.html")


@signin_required
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
                if request.user.is_superuser:  # user type
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
@signin_required
def logout_view(request):
    logout(request,)
    return redirect("login")

@signin_required
def admindashboard(request):
    return render(request, "dashboard.html")
@signin_required
def theatre_registration_view(request):
    form = AdminTheatreRegistrationForm()
    if request.method == "POST":
        form = AdminTheatreRegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, "your theatre has been added")
            return redirect("list_theatre")
        else:
            messages.error(request, " Theatre registration failed")
        return render(request, "ATR.html", {"form": form})
    return render(request, "ATR.html", {"form": form})

@signin_required
def theatre_list_view(request):
    all_theatre = Theater.objects.all()
    return render(request, "list_theatre.html", {'theatre': all_theatre})

