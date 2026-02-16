# urls.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12


from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProfileListView.as_view(), name="show_all_profiles"),
    path('mini_insta/profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
]