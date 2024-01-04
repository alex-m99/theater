from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("home", views.home), 
    path("adauga-actori", views.actors_tab),
    path("save", views.save_student),
    path("adauga-actori/add", views.save_actor),
    path("adauga-actori/update", views.update_actor),
    path("adauga-actori/delete", views.delete_actor)
]