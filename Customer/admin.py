from django.contrib import admin
from Customer.models import BookingRequest

class BookingrequestAdmin(admin.ModelAdmin):
   list_display = ["customer","show","play_time","screen","occupancy"]
admin.site.register(BookingRequest, BookingrequestAdmin)
