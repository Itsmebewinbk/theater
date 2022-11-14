from django import forms
from Theater.models import Theater, Screen


class TheatreRegistrationForm(forms.ModelForm):
    class Meta:
        model = Theater
        exclude = ("approval", "owner")
        fields = "__all__"


class TheatreEditForm(forms.ModelForm):
    class Meta:
        model = Theater
        exclude = ("approval", "owner", "theater_status")
        fields = "__all__"


class ScreenRegistrationForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = "__all__"
        exclude = ("theater",)


class ScreenEditForm(forms.ModelForm):
    class Meta:
        model = Screen
        exclude = ("theater",)
        fields = "__all__"
