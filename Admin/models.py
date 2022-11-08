from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser

class BaseUser(AbstractBaseUser):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('not specified', 'not specified'),
    )
    gender = models.CharField(choices=GENDER_CHOICES,max_length=100)
    age = models.IntegerField()
    mobile = models.CharField(max_length=12)
    address = models.TextField()
    CHOICE = ('Admin', 'Admin'), ('Customer', 'Customer'), ('Theater', 'Theater')
    usertype = models.CharField(choices=CHOICE,max_length=50)

class Theater(models.Model):
    theater_name = models.CharField(max_length=120)
    city = models.CharField(max_length=50)
    owner_name = models.OneToOneField(BaseUser, on_delete=models.CASCADE)  # one to one relation
    image = models.ImageField(max_length=120, null=True)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=12)
    Theater_status_choice=(
        ("active","active"),
        ("inactive","inactive")
    )
    theater_status=models.CharField(choices=Theater_status_choice,max_length=50)

    def __str__(self):
        return self.theater_name

class Screen(models.Model):
    screen_name=models.CharField(unique=True,max_length=100)
    Theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    entry_fee = models.IntegerField()

    options = (
        ("empty", "empty"),
        ("filling", "filling"),
        ("Housefull", "Housefull"),
        ("cancelled", "cancelled")
    )
    screen_status = models.CharField(choices=options, max_length=120, default="empty")
    total_seats = models.IntegerField()

    def __str__(self):
        return self.screen_name

class Movie(models.Model):  # singular
    poster = models.ImageField()
    movie_name=models.CharField(max_length=100)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    showtime=(
        ("Morning","Morning"),
        ("Noon","Noon"),
        ("1st","1st"),
        ("2nd","2nd")
    )
    play_time=models.CharField(choices=showtime,max_length=120)
    start_date = models.DateField()
    end_date=models.DateField()

    def __str__(self):
        return str(self.poster) + "-" + str(self.screen)

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    play_time=models.DateTimeField(auto_now_add=True)
    TotalBooking=models.PositiveIntegerField()

    def __str__(self):
        return str(self.movie) + "-"  + str(self.date)


class BookingRequest(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    show=models.ForeignKey(Show,on_delete=models.CASCADE)
    play_date_time = models.DateTimeField(auto_now_add=True)

    # available_seats = models.ForeignKey(Screen, on_delete=models.CASCADE)
