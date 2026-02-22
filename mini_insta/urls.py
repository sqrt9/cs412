# urls.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12
# Modified Feb. 20


from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='show_post'),
    path("profile/<int:pk>/create_post/", views.CreatePostView.as_view(), name="create_post"),
]