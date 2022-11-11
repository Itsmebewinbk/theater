from django.urls import path
from Admin import views
urlpatterns=[
    path("",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("user_register",views.user_registration,name="user_register"),
    path("home",views.home,name="home"),
    path("index",views.index,name="index"),
    path("dashboard",views.admindashboard,name="dashboard"),
]