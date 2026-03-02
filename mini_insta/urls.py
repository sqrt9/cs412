# urls.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12
# Modified Feb. 20
# Description
# ---
# All valid URL patterns that will resolve
# in the mini_insta app pages.
# ---


from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name='followers'),
    path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name='following'),
    path('profile/<int:pk>/feed', views.PostFeedListView.as_view(), name='feed'),
    path('profile/<int:pk>/search', views.SearchView.as_view(), name='search')
]