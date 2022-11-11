from django.contrib import admin
from Theater.models import *

class TheaterAdmin(admin.ModelAdmin):
  list_display = ("theater_name","city","owner","email_id","approval","image")
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