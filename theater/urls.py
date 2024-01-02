from django.urls import path
from . import views

urlpatterns = [
    path("actori", views.get_actors, name="actors-page"),
    path("actori/<slug:name>", views.actor_detail,
         name="actori-detail-page")
]