from django.urls import path
from Customer import views
urlpatterns=[
    path("home", views.home, name="home"),
    path("theatre", views.theatre_list, name="list-theatre"),
    path("movie_detail/<int:id>", views.movie_detail_view, name="detail_movie"),
    path("show-list/<int:id>", views.show_list, name="show-list"),
    path("morning-list", views.morning_show,name="morning-list"),
    path("noon-list", views.noon_show,name="noon-list"),
    path("1st-list", views.first_show,name="1st-list"),
    path("2nd-list", views.second_show,name="2nd-list"),
    path("show_booking/<int:id>", views.customer_booking,name="show_booking"),
    path("booked", views.booked_list,name="booked"),
    path("delete/booking/<int:id>", views.cancellation,name="cancelled"),
    path("customer-detail/<int:id>", views.customer_details,name="customer_details"),
    path("customer-detail_edit/<int:id>", views.customer_edit,name="customer_details_edit"),
    # path("email/<int:id>", views.email,name="email")

]