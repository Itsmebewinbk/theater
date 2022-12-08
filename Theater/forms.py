from django import forms
from Theater.models import Theater, Screen,Movie,Show


class TheatreRegistrationForm(forms.ModelForm):
    class Meta:
        model = Theater
        exclude = ("approval", "owner",)
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

class MovieAddForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields= "__all__"
        exclude=("screen",)
        widgets = {
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }

class ShowAddForm(forms.ModelForm):
    class Meta:
        model= Show
        fields="__all__"
        exclude=("movie","play_time","date","screen_status")

