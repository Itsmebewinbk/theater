from django.shortcuts import render, redirect
from django.contrib import messages
from Theater.forms import TheatreRegistrationForm
from Admin.models import *
def theatre_registration(request, *args, **kwargs):
    form = TheatreRegistrationForm()
    if request.method == "POST":
        form = TheatreRegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            User.objects.create_user(**form.cleaned_data)
            messages.success(request, "your account has been created")
            return redirect("login")
        else:
            messages.error(request, "registration failed")
        return render(request, "registration.html", {"form": form})
    return render(request, "registration.html", {"form": form})


