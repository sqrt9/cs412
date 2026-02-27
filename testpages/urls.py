

from django.urls import path
from . import views

urlpatterns = [
    path("", views.base, name="root"),
    path("base", views.base),
    path("grid", views.grid),
    path("grid_scrollable", views.grid_scrollable),
    ]
