from django.shortcuts import render, redirect,reverse,HttpResponseRedirect
from django.contrib import messages
from django.forms import modelformset_factory, inlineformset_factory
from Theater.forms import *
from Theater.models import *
from Admin.decorators import signin_required, theatre_login, customer_login
from django.core.exceptions import ValidationError
import datetime
from datetime import timedelta, datetime, date
from django.db import transaction
from datetime import datetime, timedelta



# -----------------------------------------THEATRE-------------------------------------------------------------------------------------------------------------------------------------------
@signin_required
@theatre_login
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
@theatre_login
def list_theatre(request, *args, **kwargs):
    all_theatre = Theater.objects.filter(owner=request.user)
    return render(request, "theatre_list.html", {'theatre': all_theatre})


@signin_required
@theatre_login
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
@theatre_login
def delete_theatre(request,id):
    Theatre = Theater.objects.get(id=id)
    Theatre.theater_status = "inactive"
    Theatre.save()
    messages.success(request, "Theatre deactivated....")
    return redirect("list_theatre")


@signin_required
@theatre_login
def view_theatre(request, id):
    theatre = Theater.objects.get(id=id)
    return render(request, "theatre_detail.html", {"theatre": theatre})


# -------------------------------------------------SCREEN---------------------------------------------------------------------------------------------------------------------------------------
@signin_required
@theatre_login
def add_screen(request, id):
    theatre = Theater.objects.get(id=id)  #
    form = ScreenRegistrationForm()
    if request.method == "POST":
        form = ScreenRegistrationForm(request.POST)
        if form.is_valid():
            for screen in Screen.objects.all().filter(theater=theatre,):
                if screen.screen_name != request.POST['screen_name']:
                    pass
                else:
                    messages.error(request, "Screen_Name already exists")
                    return render(request, "screen_registration.html", {"form": form})
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
@theatre_login
def list_screen(request,):
    all_screens = Screen.objects.filter(theater__owner=request.user)
    return render(request, "screen_list.html", {"screen": all_screens})


@signin_required
@theatre_login
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
            return redirect("list_screen",)
        else:
            msg = "Screen updation failed"
            messages.error(request, msg)
            return render(request, "screen_edit.html", {"form": form})
    return render(request, "screen_edit.html", {"form": form})


@signin_required
@theatre_login
def delete_screen(request, id):
        Screen.objects.get(id=id).delete()
        messages.success(request, "Screen deleted")
        return redirect("screen_list",)

# ---------------------------------------------------MOVIE-------------------------------------------------------------------------------------------------
@signin_required
@theatre_login
def add_show(request, id):
    context = {}
    form = MovieAddForm()
    context['form'] = form
    if request.method == "POST":
        form = MovieAddForm(request.POST, files=request.FILES)
        if form.is_valid():
            cleaned_form = form.cleaned_data
            if date.today() <= cleaned_form["start_date"] < cleaned_form["end_date"]:
                pass
            else:
                messages.error(request, "Date is not valid")
                return render(request, "movie_registration.html", context)
            shows = Show.objects.filter(movie__screen__id=id, play_time=cleaned_form["play_time"]).exclude(screen_status="cancelled")
            for show in shows:
                if cleaned_form['start_date'] <= show.date <= cleaned_form['end_date']:
                    messages.error(
                        request, "Movie already streaming")
                    return render(request, "movie_registration.html", context)

                # for movies in Movie.objects.filter(screen=screen, play_time=cleaned_form["play_time"]):
                #
                #         if str(movies.start_date) < str(request.POST['start_date']) and str(
                #                 movies.end_date) < str(request.POST['start_date']):
                #             pass
                #         elif str(movies.start_date) > str(request.POST['end_date']) and str(
                #                 movies.end_date) > str(request.POST['end_date']):
                #             pass
                #         else:
                #             messages.error(request, "Movie already streaming")
                #             return render(request, "movie_registration.html", context)


        form.cleaned_data['screen'] = Screen.objects.get(id=id)
        create_movie = Movie.objects.create(**form.cleaned_data)
     #==================================================================
        total_days = (create_movie.end_date - create_movie.start_date).days

        dates = []
        for data in range(total_days + 1):
            datas = create_movie.start_date + timedelta(days=data)
            dates.append(datas)

        # for date1 in dates:
        #     Show.objects.create(movie=create_movie,date=date1,play_time=create_movie.play_time, TotalBooking=0)
        # messages.success(request, "Show has been added")
        # return redirect("list_movie", id=id)

        show=[
            Show(movie=create_movie,
                    date=date1,
                    play_time=create_movie.play_time,
                    TotalBooking=0)
        for date1 in dates]
        Show.objects.bulk_create(show)
        messages.success(request, "Show has been added")
        return redirect("list_movie")
    return render(request, "movie_registration.html", context)

        #Atomic_Transaction
            # with transaction.atomic():
        #         show=Show(movie=create_movie,date=date1, play_time=create_movie.play_time,TotalBooking=0)
        #         show.save()

@signin_required
@theatre_login
def list_movie(request):
    all_movies = Movie.objects.filter(screen__theater__owner=request.user)
    return render(request, "movie_list.html", {"movie": all_movies})

@signin_required
@theatre_login
def delete_movie(request,id,):
    movie=Movie.objects.get(id=id)
    movie.delete()
    messages.success(request,"Movie deleted")
    return redirect("list_movie")

@signin_required
@theatre_login
def list_show(request, id):
    all_show = Show.objects.filter(movie__id=id)

    return render(request, "show_list.html", {"show": all_show})
@signin_required
@theatre_login
def cancel_show(request,id):
    show = Show.objects.get(id=id)
    show.screen_status = "cancelled"
    show.save()
    return redirect(request,"list_show",id=id)











