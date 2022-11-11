from django.db import models
from Admin.models import CustomUser

THEATRE_STATUS_CHOICE = (
    ("active", "active"),
    ("inactive", "inactive")
)
SCREEN_STATUS = (
    ("empty", "empty"),
    ("filling", "filling"),
    ("Housefull", "Housefull"),
    ("cancelled", "cancelled")
)
SHOWTIME = (
    ("Morning", "Morning"),
    ("Noon", "Noon"),
    ("1st", "1st"),
    ("2nd", "2nd")
)

class Theater(models.Model):
    theater_name = models.CharField(max_length=120,unique=True)
    city = models.CharField(max_length=50,null=True)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True,blank=True)# one to one relation
    image = models.ImageField(upload_to="images/",null=True)
    email_id = models.EmailField(verbose_name='email_address',max_length=255,unique=True)
    phone_number = models.CharField(max_length=12,null=True)
    approval=models.BooleanField('Approval',default=False)
    theater_status=models.CharField(choices=THEATRE_STATUS_CHOICE,max_length=50,default='active')

    def __str__(self):
        return self.theater_name
class Screen(models.Model):
    screen_name=models.CharField(unique=True,max_length=100)
    Theater = models.ForeignKey(Theater, on_delete=models.CASCADE,)
    entry_fee = models.IntegerField()
    screen_status = models.CharField(choices=SCREEN_STATUS, max_length=120, default="empty")
    total_seats = models.IntegerField()

    def __str__(self):
        return self.screen_name

class Movie(models.Model):  # singular
    poster = models.ImageField(upload_to="images/",null=True)
    movie_name=models.CharField(max_length=100)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    play_time=models.CharField(choices=SHOWTIME,max_length=120)
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
