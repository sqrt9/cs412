# File: voter_analytics/urls.py
# Created: Jan. 29
# Author: Theodore Harlan
#         hpt@bu.edu
# Description: url imports for quote app

from django.urls import path
from . import views

urlpatterns = [
    path("", views.VoterListView.as_view(), name="voters"),
    path("voter/<int:pk>", views.VoterDetailView.as_view(), name="voter"),
    path("graphs/", views.VoterGraphsView.as_view(), name="graphs"),
    ]
