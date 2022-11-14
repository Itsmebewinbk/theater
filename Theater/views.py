from django.shortcuts import render, redirect
from django.contrib import messages
from Theater.forms import TheatreRegistrationForm,TheatreEditForm,ScreenRegistrationForm
from Theater.models import *

#-----------------------------------------THEATRE-------------------------------------------------------------------------------------------------------------------------------------------
def add_theatre(request, *args, **kwargs):
    form = TheatreRegistrationForm()
    if request.method == "POST":
        form = TheatreRegistrationForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.owner=request.user
            form.save().id
            messages.success(request, "your theatre has been added")
            return redirect("list_theatre")
        else:
            messages.error(request, " Theatre registration failed")
        return render(request, "theatre_registration.html", {"form": form})
    return render(request, "theatre_registration.html", {"form": form})

def list_theatre(request,*args,**kwargs):
    all_theatre=Theater.objects.filter(owner=request.user)
    return render(request,"theatre_list.html",{'theatre':all_theatre})
def edit_theatre(request,*args,**kwargs):
    id=kwargs.get("id")
    theatre=Theater.objects.get(id=id,)
    form=TheatreEditForm(instance=theatre)
    if request.method=="POST":
        id = kwargs.get("id")
        theatre = Theater.objects.get(id=id)
        form = TheatreEditForm(request.POST, instance=theatre)
        if form.is_valid():
            msg = "Theatre has been edited"
            messages.success(request, msg)
            form.save()
            return redirect("list_theatre")
        else:
            msg = "Theatre updation failed"
            messages.error((request, msg))
            return render(request, "theatre_edit.html", {"form": form})
    return render(request, "theatre_edit.html", {"form": form})
def delete_theatre(request,*args,**kwargs):
    id=kwargs.get("id")
    Theatre=Theater.objects.get(id=id)
    Theatre.theater_status="inactive"
    Theatre.save()
    messages.success(request, "Theatre deactivated....")
    return redirect("list_theatre")
#-------------------------------------------------SCREEN---------------------------------------------------------------------------------------------------------------------------------------
def add_screen(request,id):
    theatre = Theater.objects.filter(id=id)
    form=ScreenRegistrationForm(instance=theatre)
    if request.method=="POST":
        form=ScreenRegistrationForm(request.POST,instance=theatre)
        if form.is_valid():
            form.cleaned_data["theater"]=theatre
            Screen.objects.create(**form.cleaned_data)
            form.save()
            # form.cleaned_data["theater"]=Theater.objects.get(owner=request.user)  #For 1 to 1 User
            # Screen.objects.create(**form.cleaned_data)
            messages.success(request,"Screen have been added")
            return redirect("list_screen")
        else:
            messages.success(request,"Screen Registration Failed")
            return render(request,"screen_registration.html",{"form":form})
    return render(request,"screen_registration.html",{"form":form})

def list_screen(request):
    all_screens=Screen.objects.all()
    return render(request, "screen_list.html", {"screen": all_screens})
# def edit_screen(request,*args,**kwargs):
#     id = kwargs.get("id")
#     screen = Screen.objects.get(id=id)
#     form = ScreenEditForm(instance=screen)
#     if request.method == "POST":
#         id = kwargs.get("id")
#         screen = Screen.objects.get(id=id)
#         form = TheatreEditForm(request.POST, instance=screen)
#         if form.is_valid():
#             msg = "Screen has been edited"
#             messages.success(request, msg)
#             form.save()
#             return redirect("list_screen")
#         else:
#             msg = "Screen updation failed"
#             messages.error((request, msg))
#             return render(request, "theatre_edit.html", {"form": form})
#     return render(request, "theatre_edit.html", {"form": form})
#
# def delete_screen(request,*args,**kwargs,):
#     id=kwargs.get("id")
#     Screen.objects.get(id=id).delete()
#     messages.success(request, "Screen deleted")
#     return redirect("screen_list")
