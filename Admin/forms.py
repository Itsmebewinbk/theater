from django import forms
from Admin.models import *
from Theater.models import Theater
from django.contrib.auth.forms import UserCreationForm


class LogInForm(forms.Form):
    username=forms.CharField(label=" ",label_suffix=" ",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))
    password=forms.CharField(label_suffix=' ',label=" ",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
