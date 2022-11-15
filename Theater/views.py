from django.shortcuts import render, redirect
from django.contrib import messages
from Theater.forms import *
from Theater.models import *
from Admin.decorators import signin_required
import datetime


# -----------------------------------------THEATRE-------------------------------------------------------------------------------------------------------------------------------------------
@signin_required
def add_theatre(request, *args, **kwargs):
    form = TheatreRegistrationForm()
    if request.method == "POST":
        form = TheatreRegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, "your theatre has been added")
            return redirect("list_theatre")
        else:
            messages.error(request, " Theatre registration failed")
        return render(request, "theatre_registration.html", {"form": form})
    return render(request, "theatre_registration.html", {"form": form})


@signin_required
def list_theatre(request, *args, **kwargs):
    all_theatre = Theater.objects.filter(owner=request.user)
    return render(request, "theatre_list.html", {'theatre': all_theatre})


@signin_required
def edit_theatre(request, *args, **kwargs):
    id = kwargs.get("id")
    theatre = Theater.objects.get(id=id, )
    form = TheatreEditForm(instance=theatre)
    if request.method == "POST":
        id = kwargs.get("id")
        theatre = Theater.objects.get(id=id)
        form = TheatreEditForm(request.POST, instance=theatre)
        if form.is_valid():
            msg = "Theatre has been edited"
            messages.success(request, msg)
            form.save()
            return redirect("list_theatre")
        else:
            msg = "Theatre updation failed"
            messages.error((request, msg))
            return render(request, "theatre_edit.html", {"form": form})
    return render(request, "theatre_edit.html", {"form": form})


@signin_required
def delete_theatre(request, *args, **kwargs):
    id = kwargs.get("id")
    Theatre = Theater.objects.get(id=id)
    Theatre.theater_status = "inactive"
    Theatre.save()
    messages.success(request, "Theatre deactivated....")
    return redirect("list_theatre")


@signin_required
def view_theatre(request, id):
    theatre = Theater.objects.get(id=id)
    return render(request, "theatre_detail.html", {"theatre": theatre})


# -------------------------------------------------SCREEN---------------------------------------------------------------------------------------------------------------------------------------
@signin_required
def add_screen(request, id):
    theatre = Theater.objects.get(id=id)  #
    form = ScreenRegistrationForm()
    if request.method == "POST":
        form = ScreenRegistrationForm(request.POST)
        if form.is_valid():
            form.cleaned_data["theater"] = theatre
            Screen.objects.create(**form.cleaned_data)
            # form.cleaned_data["theater"]=Theater.objects.get(owner=request.user)  #For 1 to 1 User
            # Screen.objects.create(**form.cleaned_data)
            messages.success(request, "Screen have been added")
            return redirect("list_screen", id=id)
        else:
            messages.success(request, "Screen Registration Failed")
            return render(request, "screen_registration.html", {"form": form})
    return render(request, "screen_registration.html", {"form": form})


@signin_required
def list_screen(request, id):
    theatre = Theater.objects.get(id=id)
    all_screens = Screen.objects.filter(theater=theatre)
    return render(request, "screen_list.html", {"screen": all_screens})


@signin_required
def edit_screen(request, id):
    screen = Screen.objects.get(id=id)
    form = ScreenEditForm(instance=screen)
    if request.method == "POST":
        screen = Screen.objects.get(id=id)
        form = ScreenEditForm(request.POST, instance=screen)
        if form.is_valid():
            msg = "Screen has been edited"
            messages.success(request, msg)
            form.save()
            return redirect("list_screen", id=id)
        else:
            msg = "Screen updation failed"
            messages.error(request, msg)
            return render(request, "screen_edit.html", {"form": form})
    return render(request, "screen_edit.html", {"form": form})


@signin_required
def delete_screen(request, id):
    Screen.objects.get(id=id).delete()
    messages.success(request, "Screen deleted")
    return redirect("screen_list", id=id)


# ---------------------------------------------------MOVIE-------------------------------------------------------------------------------------------------
@signin_required
def add_movie(request, id):
    screen = Screen.objects.filter(id=id)
    form = MovieAddForm()
    if request.method == "POST":
        form = MovieAddForm(request.POST, files=request.FILES)
        for i in screen.iterator():
            if Movie.play_time(i) != Movie.play_time(
                    i + 1) and Movie.start_date >= datetime.date.today() and Movie.start_date < Movie.end_date:
                pass
            else:
                messages.error(request, "Movie registration failed")

        if form.is_valid():
            form.cleaned_data['screen'] = Screen.objects.get(id=id)
            Movie.objects.create(**form.cleaned_data)
            messages.success(request, "Movie has been added")
            return redirect("list_movie", id=id)
        else:
            messages.error(request, " Movie registration failed")
        return render(request, "movie_registration.html", {"form": form})
    return render(request, "movie_registration.html", {"form": form})


@signin_required
def list_movie(request, id):
    screen = Screen.objects.get(id=id)
    all_movies = Movie.objects.filter(screen=screen)
    return render(request, "movie_list.html", {"movie": all_movies})
