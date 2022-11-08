from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser

class BaseUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('not specified', 'not specified'),
    )
    gender = models.CharField(choices=GENDER_CHOICES)
    age = models.IntegerField()
    mobile = models.CharField(max_length=12)
    address = models.TextField()
    CHOICE = ('Admin', 'Admin'), ('Customer', 'Customer'), ('Theater', 'Theater')
    usertype = models.CharField(choices=CHOICE)

class Theater(models.Model):
    CITY_CHOICE = (
        ('Kochi', 'Kochi'),
        ('Thrissur', 'Thrissur'),
        ('Trivandram', 'Trivandram'),
        ('Chennai', 'Chennai'),
        ('Bangalore', 'Bangalore'),
        ('Ahmedabad', 'Ahmedabad'),
    )
    city = models.CharField(max_length=9, choices=CITY_CHOICE, null=False)
    theater_name = models.CharField(max_length=120)
    owner_name = models.OneToOneField(User, on_delete=models.CASCADE)  # one to one relation
    image = models.ImageField(max_length=120, null=True)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.theater_name

class Screen(models.Model):
    screen_name = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie = models.CharField(max_length=120, unique=True)
    entry_fee = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    options = (
        ("empty", "empty"),
        ("filling", "filling"),
        ("Housefull", "Housefull"),
        ("cancelled", "cancelled")
    )
    screen_status = models.CharField(choices=options, max_length=120, default="empty")
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def booked_seats(self):
        booked_seats = self.total_seats - self.available_seats
        return booked_seats

    def __str__(self):
        return self.screen_name

class Movie(models.Model):  # singular
    poster = models.ImageField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    start_time=models.DateTimeField(auto_now_add=True)
    end_time=models.DateTimeField()

    def __str__(self):
        return str(self.poster) + "-" + str(self.screen) + "-" + str(self.theater)

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theater, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.movie) + "-" + str(self.theatre) + "-" + str(self.date) + "-" + str(self.time)


class BookingRequest(models.Model):
    customer = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    screen_name = models.ForeignKey(Screen, on_delete=models.CASCADE)
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show=models.ForeignKey
    play_date_time = models.DateTimeField(auto_now_add=True)
    available_seats = models.ForeignKey(Screen, on_delete=models.CASCADE)
