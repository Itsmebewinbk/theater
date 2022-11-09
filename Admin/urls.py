from django.urls import path
from Admin import views
urlpatterns=[
    path("",views.login_view,name="login"),
]