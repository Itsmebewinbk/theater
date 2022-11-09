from django import forms
from Theater.models import Theater
class TheatreRegistrationForm(forms.ModelForm):
    class Meta:
        model= Theater
        fields="__all__"

