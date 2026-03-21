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

from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='show_post'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('post/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('profile/<int:pk>/followers/', views.ShowFollowersDetailView.as_view(), name='followers'),
    path('profile/<int:pk>/following/', views.ShowFollowingDetailView.as_view(), name='following'),
    path('profile/feed/', views.PostFeedListView.as_view(), name='feed'),
    path('profile/search/', views.SearchView.as_view(), name='search'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logged-out/', TemplateView.as_view(template_name='mini_insta/logged_out.html'), name='logout_confirmation'),
    path("create_profile/", views.CreateProfileView.as_view(), name="create_profile"),
    path("profile/", views.MyProfileView.as_view(), name="my_profile"),
    path("profile/<int:pk>/follow", views.FollowView.as_view(), name="follow"),
    path("profile/<int:pk>/delete_follow", views.DeleteFollowView.as_view(), name="delete_follow"),
    path("post/<int:pk>/like", views.LikeView.as_view(), name="like"),
    path("post/<int:pk>/delete_like", views.DeleteLikeView.as_view(), name="delete_like")
]