from django.contrib import admin
from Customer.models import BookingRequest

class BookingrequestAdmin(admin.ModelAdmin):
    class Meta:
        model = BookingRequest
admin.site.register(BookingRequest, BookingrequestAdmin)
