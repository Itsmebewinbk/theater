from celery import shared_task
import os
from Customer.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from THeaTRe_BooKiNG_aPP.celery import app

@shared_task(bind=True)
def send_emails(request):
    show = Show.objects.get(id=id)
    customer=CustomUser.objects.filter(id=request.user.id)
    email=[emails.email for emails in customer]
    path = os.getcwd()
    booked = BookingRequest.objects.filter(show=show)
    filename = path + show.movie.poster.url
    template = get_template('show_booked.html')
    msg = EmailMultiAlternatives( "Show Booked",None,'mindlesspeople1217@gmail.com', email,)
    msg.attach_alternative(template.render({"booked":booked}), "text/html")
    msg.attach_file(filename)
    msg.send()
    return "Done"