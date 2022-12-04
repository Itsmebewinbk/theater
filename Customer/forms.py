from django import forms
from Customer.models import BookingRequest
from Admin.models import CustomUser


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields =("occupancy",)

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model= CustomUser
        fields =("image","mobile","gender","first_name","last_name","age","address","email")
