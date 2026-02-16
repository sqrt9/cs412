

from django.urls import path
from . import views

urlpatterns = [
    path("", views.base),
    path("base", views.base),
    path("grid", views.grid),
    path("grid_scrollable", views.grid_scrollable),
    ]
