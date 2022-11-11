from django import forms
from Admin.models import *
from Theater.models import Theater
from django.contrib.auth.forms import UserCreationForm


class LogInForm(forms.Form):
    username=forms.CharField(label=" ",label_suffix=" ",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))
    password=forms.CharField(label_suffix=' ',label=" ",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password",label_suffix=" ",widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(label="Confirm Password ",label_suffix=" ", widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))
    class Meta:
        model=CustomUser
        fields=("first_name","last_name","username","email","image","mobile","gender","age","usertype")