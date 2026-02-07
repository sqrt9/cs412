# file urls.py
# created feb 6
# author hpt@bu.edu
# description url exports for restaurant app


from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("/", views.main, name="main"),
    path("main/", views.main, name="main"),
    path("order/", views.order, name="order"),
    path("confirmation/", views.confirmation, name="confirmation"),
    ]
