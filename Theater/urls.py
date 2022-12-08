from django.urls import path
from Theater import views

urlpatterns = [
    path("theatre", views.list_theatre, name="list_theatre"),
    path("theatre/add", views.add_theatre, name="add_theatre"),
    path("theatre/detail/<int:id>", views.view_theatre, name="detail_theatre"),
    path("theatre/edit/<int:id>", views.edit_theatre, name="edit_theatre"),
    path("theatre/deactivate/<int:id>", views.delete_theatre, name="del_theatre"),
    path("screen/", views.list_screen, name="list_screen"),
    path("screen/add/<int:id>", views.add_screen, name="add_screen"),
    path("screen/edit/<int:id>", views.edit_screen, name="edit_screen"),
    path("screen/delete/<int:id>", views.delete_screen, name="delete_screen"),
    path("Movie/add/<int:id>", views.add_show, name="add_movie"),
    path("Movie", views.list_movie, name="list_movie"),
    path("Movie/del/<int:id>", views.delete_movie, name="delete_movie"),
    path("Show/list/<int:id>", views.list_show, name="list_show"),
    path("Show/cancel/<int:id>", views.cancel_show, name="cancel_show"),
]
