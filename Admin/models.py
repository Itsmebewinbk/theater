from django.db import models
from django.contrib.auth.models import User

class Seats(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    total_seats=models.IntegerField()

class Screen(models.Model):
    screen_name=models.CharField(max_length=120,unique=True)
    movie=models.CharField(max_length=120,unique=True)
    entry_fee=models.IntegerField()
    seats_booked=models.ForeignKey(Seats,on_delete=models.CASCADE)
    options = (
        ("empty", "empty"),
        ("filling", "filling"),
        ("Housefull", "Housefull"),
        ("cancelled", "cancelled")
    )
    screen_status = models.CharField(choices=options, max_length=120, default="empty")


class Theater(models.Model):
    theater_name=models.CharField(max_length=120)
    owner_name = models.CharField(max_length=120, unique=True)
    image = models.ImageField(max_length=120, null=True)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=12)
    screen=models.ForeignKey(Screen,on_delete=models.CASCADE)

class Movies(models.Model):
    poster = models.ImageField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)

class BookingRequest(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    screen_name=models.ForeignKey(Screen,on_delete=models.CASCADE)
    movie_name=models.ForeignKey(Movies,on_delete=models.CASCADE)
    play_date_time=models.DateTimeField(auto_now_add=True)
    available_seats=models.ForeignKey(Seats,on_delete=models.CASCADE)


