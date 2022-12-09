from django.shortcuts import render, redirect, reverse
from Theater.models import *
from Customer.models import *
from Customer.forms import BookingForm,CustomerEditForm
from django.contrib import messages
from Admin.decorators import signin_required, theatre_login, customer_login, admin_login
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives,EmailMessage
from datetime import time, date
import datetime
from django.template.loader import get_template
from Customer.tasks.task import send_emails
import os




@signin_required
@customer_login
def home(request, *args, **kwargs):
    all_movie = Movie.objects.all()
    return render(request, "home.html", {"movies": all_movie})

@signin_required
@customer_login
def movie_detail_view(request, id):
    movies = Movie.objects.get(id=id)
    return render(request, "customer_movie_detail.html", {"movie": movies})

@signin_required
@customer_login
def theatre_list(request):
    all_theatre = Theater.objects.exclude(theater_status="inactive").exclude(approval=False)
    return render(request, "customer_theatre_list.html", {'theatre': all_theatre})

@signin_required
@customer_login
def show_list(request, id):
    movies = Movie.objects.get(id=id)
    show = Show.objects.filter(movie=movies).exclude(screen_status="cancelled")
    showss=[shows for shows in show if shows.date>=date.today()]
    # for shows in show:
    #     if shows.date >= date.today():
    #         showss.append(shows)
    #     else:
    #         messages.error(request, "NO SHOW")
    return render(request, "customer_movies_list.html", {"show": showss})

@signin_required
@customer_login
def customer_booking(request, id):
    form = BookingForm()
    show = Show.objects.get(id=id)  # 9,13,17,21
    screen = Screen.objects.get(movie__show__id=id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = BookingRequest.objects.filter(show=show)
            total_occupancy = form.cleaned_data["occupancy"]
            if BookingRequest.objects.filter(customer=request.user,show=show).count() < 5:
                pass
            else:
                messages.error(request, "Booking Limit Reached")
                return render(request, "booking.html", {"form": form})
            for data in booking:
                total_occupancy += (data.occupancy)
            seats_left=screen.total_seats-(total_occupancy - form.cleaned_data['occupancy'])
            if screen.total_seats >= total_occupancy:
                pass
            else:
                if screen.total_seats - (total_occupancy - form.cleaned_data["occupancy"])==0:
                    msg=("Seats filled")
                else:
                    msg = (f"Seats Left: {seats_left}")
                messages.error(request, msg)
                return render(request, "booking.html", {"form": form})
            if total_occupancy == 0 :
                show.screen_status = "empty"
            elif total_occupancy == screen.total_seats:
                show.screen_status = "housefull"
            elif total_occupancy-1 >= screen.total_seats // 2:
                show.screen_status = "almostfull"
            elif total_occupancy > 0:
                show.screen_status = "filling"
            show.TotalBooking=total_occupancy
            show.save()

            for i in Show.objects.filter(id=show.id):
                if str(i.date) == str(date.today()):
                    # datetime.datetime.hour
                    if (i.play_time=="Morning") and str(time(9))>  str(datetime.datetime.now().strftime('%H:%M:%S')) :
                            pass
                    elif (i.play_time == "Noon") and str(time(13))> str(datetime.datetime.now().strftime('%H:%M:%S')):
                            pass
                    elif (i.play_time == "1st") and str(time(17))> str(datetime.datetime.now().strftime('%H:%M:%S')):
                            pass
                    elif (i.play_time == "2nd") and str(time(21))> str(datetime.datetime.now().strftime('%H:%M:%S')):
                            pass
                    else:
                        messages.error(request, "Movie already streaming")
                        return render(request, "booking.html", {"form": form})
                elif  str(i.date) < str(date.today()):
                    messages.error(request, "Show expired")
                    return render(request, "booking.html", {"form": form})

            form.cleaned_data["play_time"]=show.play_time
            form.cleaned_data["customer"] = request.user
            form.cleaned_data["screen"] = screen
            form.cleaned_data["show"] = show
            BookingRequest.objects.create(**form.cleaned_data)
            send_emails.delay(id)
            
            # movie= Movie.objects.values("movie_name").filter(show__id=show.id).values_list("movie_name",flat=True)
            # show= Show.objects.filter(id=show.id)

           
            # send_mail("Show Booked",
            #             None,
            #             'mindlesspeople1217@gmail.com',
            #             ('vbgd10@gmail.com',),
            #             fail_silently=False,gin
            #             html_message=template
            #           )
            return redirect("booked")
        else:
            messages.success(request, "Booking Failed")
            return render(request, "booking.html", {"form": form})

    return render(request, "booking.html", {"form": form})

# @shared_task(bind=True)
# def email(request):
#     show = Show.objects.get(id=id)
#     customer=CustomUser.objects.filter(id=request.user.id)
#     email=[emails.email for emails in customer]
#     path = os.getcwd()
#     booked = BookingRequest.objects.filter(show=show)
#     filename = path + show.movie.poster.url
#     template = get_template('show_booked.html')
#     msg = EmailMultiAlternatives( "Show Booked",None,'mindlesspeople1217@gmail.com', email,)
#     msg.attach_alternative(template.render({"booked":booked}), "text/html")
#     msg.attach_file(filename)
#     msg.send()
    

@signin_required
@customer_login
def cancellation(request,id):
    booking = BookingRequest.objects.get(id=id)
    if booking.delete():
        for show in Show.objects.filter(bookingrequest__id=booking.id):
            outcome=show.TotalBooking-booking.occupancy
            show.TotalBooking=show.TotalBooking-booking.occupancy
            if  outcome == 0:
                show.screen_status = "empty"
                show.save()
            elif outcome - 1 >= show.movie.screen.total_seats // 2:
                show.screen_status = "almostfull"
                show.save()
            elif outcome > 0:
                show.screen_status = "filling"
                show.save()
    else:
        messages.error(request, "Error")
    # customer = CustomUser.objects.filter(id=request.user.id)
    # email = [emails.email for emails in customer]
    # template = get_template('show_cancelled.html')
    # msg = EmailMultiAlternatives("Show Cancelled", "Your show have been cancelled succefully", 'mindlesspeople1217@gmail.com', email, )
    # msg.attach_alternative(template.render({"booked": booking}), "text/html")
    # msg.send()
    messages.success(request, "Booking Cancelled")
    return redirect("booked")
    
@signin_required
@customer_login
def booked_list(request):
    booked=BookingRequest.objects.filter(customer=request.user)
    return render(request, "booked_list.html", {"booked": booked})

@signin_required
@customer_login
def morning_show(request):
    movie = Movie.objects.filter(play_time="Morning")
    return render(request, "morning_list.html", {"movie": movie})
@signin_required
@customer_login
def noon_show(request):
    movie = Movie.objects.filter(play_time="Noon")
    return render(request, "noon_list.html", {"movie": movie})
@signin_required
@customer_login
def first_show(request):
    movie = Movie.objects.filter(play_time="1st")
    return render(request, "1st_list.html", {"movie": movie})
@signin_required
@customer_login
def second_show(request):
    movie = Movie.objects.filter(play_time="2nd")
    return render(request, "2nd_list.html", {"movie": movie})
@signin_required
@customer_login
def customer_details(request,id):
    CustomUser.objects.filter(id=request.user.id)
    return render(request,"customer_details.html",)

@signin_required
@customer_login   
def customer_edit(request,id):
    # CustomUser.objects.filter(id=request.user.id)
    form=CustomerEditForm(instance=request.user)
    if request.method == "POST":
        form=CustomerEditForm(request.POST,files=request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Changed Succesfully")
            return redirect("customer_details",id=id)
        else:
            messages.success(request,"Edit Failed")
            return render(request,"customer_details_edit.html",{"form":form})
    return render(request, "customer_details_edit.html", {"form":form})



# Theatrename, Movie name, image,showtime--email
