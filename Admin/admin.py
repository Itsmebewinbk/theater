from django.contrib import admin
from Admin.models import *

admin.site.register(BaseUser)

class TheaterAdmin(admin.ModelAdmin):
  list_display = ("theater_name","city","owner_name","email_id",)
admin.site.register(Theater, TheaterAdmin)

class ScreenAdmin(admin.ModelAdmin):
    class Meta:
        model = Screen
admin.site.register(Screen,ScreenAdmin)

class MovieAdmin(admin.ModelAdmin):
    class Meta:
        model = Movie
admin.site.register(Movie, MovieAdmin)


class ShowAdmin(admin.ModelAdmin):
    class Meta:
        model = Show
admin.site.register(Show, ShowAdmin)

class BookingrequestAdmin(admin.ModelAdmin):
    class Meta:
        model = BookingRequest
admin.site.register(BookingRequest, BookingrequestAdmin)
