# File: quotes/urls.py
# Created: Jan. 29
# Author: Theodore Harlan
#         hpt@bu.edu
# Description: url imports for quote app

from django.urls import path
from . import views

urlpatterns = [
    path("", views.quote, name="home"),
    path("quote/", views.quote, name="quote"),
    path("show_all/", views.show_all, name="show_all"),
    path("about/", views.about, name="about")
    ]

