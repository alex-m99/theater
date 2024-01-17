from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("home", views.home), 
    path("adauga-actori", views.actors_tab, name='actors_tab'), 
    path("adauga-actori/add", views.save_actor),
    path("adauga-actori/update", views.update_actor),
    path("adauga-actori/delete", views.delete_actor),
    path("adauga-actori/search", views.search_actor),

    path("adauga-suport", views.support_tab, name='support_tab'), 
    path("adauga-suport/add", views.save_support),
    path("adauga-suport/update", views.update_support),
    path("adauga-suport/delete", views.delete_support),

    path("adauga-piese", views.plays_tab, name='plays_tab'), 
    path("adauga-piese/add", views.save_play),
    path("adauga-piese/update", views.update_play),
    path("adauga-piese/delete", views.delete_play),

    path("adauga-spectacole", views.shows_tab, name='shows_tab'),
    path("adauga-spectacole/add", views.save_show),
    path("adauga-spectacole/update", views.update_show),
    path("adauga-spectacole/delete", views.delete_show),
]