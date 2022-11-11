from django.db import models
from Admin.models import CustomUser
from Theater.models import Show

class BookingRequest(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    show=models.ForeignKey(Show,on_delete=models.CASCADE)
    play_date_time = models.DateTimeField(auto_now_add=True)

    # available_seats = models.ForeignKey(Screen, on_delete=models.CASCADE)
