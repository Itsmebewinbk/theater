from django.shortcuts import render
from Admin.models import BaseUser
def authenticate(*args,**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user_data=[user for user in BaseUser() if user["username"]==username and user["password"]== password]
    return user_data
