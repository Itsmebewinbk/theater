from django.db import models
from Admin.models import CustomUser
from Theater.models import Show,Screen
from django.core.validators import MinValueValidator,MaxValueValidator
SHOWTIME = (
    ("Morning", "Morning"),
    ("Noon", "Noon"),
    ("1st", "1st"),
    ("2nd", "2nd")
)
class BookingRequest(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    show=models.ForeignKey(Show,on_delete=models.CASCADE)
    play_time = models.CharField(choices=SHOWTIME, max_length=120)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    occupancy=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

