from django.urls import path
from . import views

urlpatterns = [
    path("actori", views.get_actors, name="actors-page"),
]