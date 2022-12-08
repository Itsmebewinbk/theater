from django.contrib import admin
from Theater.models import *

class TheaterAdmin(admin.ModelAdmin):
  list_display = ("theater_name","city","owner","email_id","approval","image")
admin.site.register(Theater, TheaterAdmin)

class ScreenAdmin(admin.ModelAdmin):
    list_display = ("screen_name","theater","total_seats")
admin.site.register(Screen,ScreenAdmin)

class MovieAdmin(admin.ModelAdmin):
   list_display = ("movie_name","screen","play_time","start_date","end_date")
admin.site.register(Movie, MovieAdmin)


class ShowAdmin(admin.ModelAdmin):
    list_display = ("movie","screen_status","date","play_time","TotalBooking")
admin.site.register(Show, ShowAdmin)

