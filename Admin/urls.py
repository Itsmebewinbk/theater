from django.urls import path
from Admin import views
urlpatterns=[
    path("",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("customer_user_register",views.customer_user_registration,name="c_user_register"),
    path("theater_user_register",views.theater_user_registration,name="t_user_register"),
    path("index",views.index,name="index"),
    path("dashboard",views.admindashboard,name="dashboard"),
    path("theatre/add",views.theatre_registration_view,name="addTheatre"),
    path("theatre",views.theatre_list_view,name="listTheatre"),
    path("theatre/edit/<int:id>",views.admin_edit_theatre,name="editTheatre"),
    path("theatre/approval_list",views.admin_approval_list,name="approve_list"),
    path("theatre/approve/<int:id>",views.admin_approval,name="approve"),
    path("theatre/rejected/<int:id>",views.reject,name="reject"),
    path("theatre/activate/<int:id>",views.activate,name="activate"),
    path("theatre/deactivate/<int:id>",views.deactivate,name="deactivate"),
]