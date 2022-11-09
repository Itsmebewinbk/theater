from django.urls import path
from Theater import views
urlpatterns=[
    path("", views.theatre_registration, name="register"),

]
