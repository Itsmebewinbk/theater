from django.shortcuts import render, redirect, reverse
from Admin.forms import LogInForm, RegistrationForm
from Admin.forms import AdminTheatreRegistrationForm,AdminTheatreEditForm
from Theater.models import Theater, Screen, Movie, Show
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Admin.decorators import signin_required, theatre_login, customer_login, admin_login
from Admin.models import *


@signin_required
@theatre_login
def index(request,):
    all_movie = Movie.objects.filter(screen__theater__owner=request.user)
    return render(request, "index.html", {"movie": all_movie})



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


def customer_user_registration(request,*args,**kwargs):
    form = RegistrationForm()
    kwargs["usertype"]="customer"
    if request.method == "POST":
        form = RegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            user = CustomUser.objects.create_user(**form.cleaned_data, **kwargs)
            user.set_password(form.cleaned_data.get('password'))
            messages.success(request, "your account has been created")
            return redirect("login")
    else:
        messages.error(request, "registration failed")
        return render(request, "registration.html", {"form": form})
    return render(request, "registration.html", {"form": form})


def theater_user_registration(request,*args,**kwargs):
    form = RegistrationForm()
    kwargs["usertype"]="theater"
    if request.method == "POST":
        form = RegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            user=CustomUser.objects.create_user(**form.cleaned_data,**kwargs)
            user.set_password(form.cleaned_data.get('password'))
            messages.success(request, "your account has been created")
            return redirect("login")
        else:
            messages.error(request, "registration failed")
            return render(request, "registration.html", {"form": form})
    return render(request, "registration.html", {"form": form})


@signin_required
def logout_view(request):
    logout(request, )
    return redirect("login")


@admin_login
@signin_required
def admindashboard(request):
    approval_theatre = Theater.objects.filter(approval=False)
    cnt = approval_theatre.count()
    cnt1 = Theater.objects.all().count()
    context = {}
    context["count"] = cnt
    context["count1"] = cnt1
    return render(request, "dashboard.html",context)

@admin_login
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


@admin_login
@signin_required
def theatre_list_view(request):
    all_theatre = Theater.objects.all()
    return render(request, "list_theatre.html", {'theatre': all_theatre})
@admin_login
@signin_required
def admin_edit_theatre(request,id):
    theatre = Theater.objects.get(id=id)
    form = AdminTheatreEditForm(instance=theatre)
    if request.method == "POST":
        theatre = Theater.objects.get(id=id)
        form = AdminTheatreEditForm(request.POST, instance=theatre)
        if form.is_valid():
            msg = "Theatre has been edited"
            messages.success(request, msg)
            form.save()
            return redirect("listTheatre")
        else:
            msg = "Theatre updation failed"
            messages.error((request, msg))
            return render(request, "admin_theatre_edit.html", {"form": form})
    return render(request, "admin_theatre_edit.html", {"form": form})

def admin_approval_list(request):
    approval_theatre = Theater.objects.filter(approval=False)
    return render(request, "approval_list_theatre.html", {'approve': approval_theatre})

def admin_approval(request,id):
    theatre=Theater.objects.get(id=id)
    theatre.approval=True
    theatre.save()
    messages.success(request, "Theatre approved....")
    return redirect("approve_list")

def activate(request,id):
    theatre=Theater.objects.get(id=id)
    theatre.theater_status="active"
    theatre.save()
    messages.success(request, "Theatre Activated....")
    return redirect("listTheatre")
def deactivate(request,id):
    theatre=Theater.objects.get(id=id)
    theatre.theater_status="inactive"
    theatre.save()
    messages.success(request, "Theatre Deactivated....")
    return redirect("listTheatre")
def reject(request,id):
    theatre = Theater.objects.get(id=id)
    theatre.delete()
    messages.success(request, "Theatre Deleted....")
    return redirect("approve_list")




