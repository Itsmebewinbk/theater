from celery import shared_task
import os
from Customer.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from THeaTRe_BooKiNG_aPP.celery import app

import datetime

@shared_task(bind=True)
def send_email(request,id):
    show = Show.objects.get(id=id)
    book=BookingRequest.objects.get(show__id=id)
    emails=[book.customer.email]
    path = os.getcwd()
    booked = BookingRequest.objects.filter(show=show)
    filename = path + show.movie.poster.url
    template = get_template('show_booked.html')
    msg = EmailMultiAlternatives( "Show Booked",None,'mindlesspeople1217@gmail.com', emails)
    msg.attach_alternative(template.render({"booked":booked}), "text/html")
    msg.attach_file(filename)
    msg.send()
    return "Done"

@shared_task()
def delete_shows():
    show = Show.objects.all()
    for shows in show:
        if  shows.date < datetime.date.today():
            shows.delete()
    return "Deleted"