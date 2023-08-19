from django.shortcuts import redirect
from django.contrib import messages


def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return fn(request, *args, **kwargs)
        else:
            messages.error(request, "You must Login")
            return redirect("login")

    return wrapper


def theatre_login(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.usertype == "theater":
            return fn(request, *args, **kwargs)
        else:
            messages.error(request, "You must Login")
            return redirect("login")

    return wrapper


def customer_login(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.usertype == "customer":
            return fn(request, *args, **kwargs)
        else:
            messages.error(request, "You must Login")
            return redirect("login")

    return wrapper


def admin_login(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return fn(request, *args, **kwargs)
        else:
            messages.error(request, "You must Login")
            return redirect("login")

    return wrapper
