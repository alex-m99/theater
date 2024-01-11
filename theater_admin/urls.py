from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("home", views.home), 
    path("save", views.save_student),
    path("adauga-actori", views.actors_tab, name='actors_tab'), 
    path("adauga-actori/add", views.save_actor),
    path("adauga-actori/update", views.update_actor),
    path("adauga-actori/delete", views.delete_actor),
    path("adauga-actori/search", views.search_actor),
    path("adauga-suport", views.support_tab, name='support_tab'), 
    path("adauga-suport/add", views.save_support),
    path("adauga-spectacole", views.shows_tab, name='shows_tab'),
    path("adauga-spectacole/add", views.save_show)
]