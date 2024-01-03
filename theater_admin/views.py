from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.


def home(request):
    return render(request, "home.html", {
        "current_tab": "home"
    })

def readers(request):
    return render(request, "readers.html", {
        "current_tab": "readers"
    })

def shopping(request):
    return HttpResponse("Welcome to shopping")

def save_student(request):
    student_name = request.POST["student_name"]
    return  render(request, "welcome.html", {
        "student_name": student_name
    })

def readers_tab(request):
    # readers = (code to read all readers)
    return render(request, "redears.html", {
        "current_tab": "readers",
        "readers": readers,
    })

def save_reader(request):
   # reader_item = reader() (code to UPDATE the reader table)
    #after the reader is saved, the url is redirected to the readers tab
    return redirect("/readers")