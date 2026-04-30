from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.base, name="root"),
    
    # unused views to preview css
    # ---
    path("base", views.base, name="base"),
    path("grid", views.grid, name="grid"),
    path("grid_scrollable", views.grid_scrollable),
    # ---
    
    path("create_account/", views.CreateAccountView.as_view(), name="create_account"),
    path("login/", auth_views.LoginView.as_view(template_name="testpages/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="logged-out"), name="logout"),
    path("logged-out/", TemplateView.as_view(template_name="testpages/logged_out.html"), name="logged-out"),
    path("upload_tracks/", views.TrackUploadView.as_view(), name="upload_tracks"),
    path("uploaded_tracks/", views.UploadedTracksListView.as_view(), name="uploaded_tracks"),
    path("my_albums/", views.ProfileAlbumsListView.as_view(), name="my_albums"),
    path("my_albums/album/<int:pk>/", views.ProfileSingleAlbumDetailView.as_view(), name="my_album"),
    path("my_albums/album/<int:pk>/delete/", views.DeleteAlbumView.as_view(), name="delete_album"),
    path("my_artists/", views.ProfileArtistsListView.as_view(), name="my_artists"),
    path("my_artists/artist/<int:pk>/", views.ProfileSingleArtistDetailView.as_view(), name="my_artist"),
    path("users/update_profile/", views.ProfileUpdateView.as_view(), name="update_profile"),
    path("users/<str:username>/", views.ProfileDetailView.as_view(), name="profile"),
    path('search/', views.search_view, name='search'),
    path("my_albums/album/<int:pk>/delete/", views.DeleteAlbumView.as_view(), name="delete_album"),
    

    ]
