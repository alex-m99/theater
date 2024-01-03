from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("home", views.home), 
    path("readers", views.readers),
    path("save", views.save_student),
    path("readers/add", views.save_reader)
]