from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.db.models import Q
from .models import *
from .forms import *
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import redirect

# views.py
# Theodore Harlan
# created april 20
# Modified april 30
# All views for django music web app.



# Create your views here.

context = {}


def base(request : HttpRequest):
    """
    Simple root page. Add a context if we're browsing on "/" to show
    public albums arranged in a grid.
    """
    context = {}
    if request.user.is_authenticated:
        profile_url = reverse('profile', kwargs={'username': request.user.username})
        context["profile_url"] = profile_url
    
    public_albums = Album.objects.filter(
        Q(is_private=False) | Q(uploader__isnull=True)
    ).distinct()
    
    context["public_albums"] = public_albums
    context["is_root"] = True
    
    return render(request, template_name="testpages/base.html", context=context)


class CreateAccountView(CreateView):
    """
    Create an account on the site. 
    Use a User and Profile form, as before.
    """
    model = Profile
    form_class = CreateAccountForm
    template_name="testpages/create_account.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_form"] = kwargs.get("account_form", UserCreationForm())
        return context
    
    def form_valid(self, form):
        account_form = UserCreationForm(self.request.POST)
        if not account_form.is_valid():
            return self.render_to_response(
                self.get_context_data(account_form=account_form)
            )
        user = account_form.save()
        login(
            request = self.request,
            user    = user,
            backend = "django.contrib.auth.backends.ModelBackend"
        )
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.object.user.username})


class TrackUploadView(LoginRequiredMixin, CreateView):
    """
    Use the multiple file upload (exactly from django's docs)
    to upload multiple files. Then, populate those files.
    """
    model = Track
    form_class = FileFieldForm
    template_name = "testpages/upload_tracks.html"
    
    def form_valid(self, form):
        files = form.cleaned_data["file_field"]

        is_private  = True if self.request.POST.get("private") else False
        from_file   = True if self.request.POST.get("from_file") else False
        search      = True if self.request.POST.get("search") else False
        form_album  = self.request.POST.get("album_name", None)
        form_artist = self.request.POST.get("artist", None)
        
        self.updated = set() 
        track_list = []
        
        for f in files:
            track = Track.objects.create(track_file=f)
            updated_album = track.populate(
                user=self.request.user.django_user,
                private=is_private,
                from_file=from_file,
                search=search
            )
            
            if updated_album:
                self.updated.add(updated_album.pk)
            
            if search:
                track_list.append((track.track_title, track))
        
        if search:
            if not from_file:
                # proceed from form info
                tag_tracks_from_info(form_album,
                                        form_artist,
                                        track_list,
                                        self.request.user.django_user,
                                        is_private)
            else:
                albums_to_tracks = {}
                for title, track in track_list:
                    if track.album not in albums_to_tracks:
                        albums_to_tracks[track.album] = []
                    albums_to_tracks[track.album].append((title, track))
                
                for album, tracks in albums_to_tracks.items():
                    if album.name != "My Songs" and album.artist.name != "Various Artists":
                        tag_tracks_from_info(form_album,
                                            form_artist,
                                            tracks, 
                                            self.request.user.django_user,
                                            is_private)
                    else:
                        print(f"Skipping search for fallback album: {album.name}")


            for title, track in track_list:
                track.refresh_from_db()
                if track.album:
                    self.updated.add(track.album.pk)

        return HttpResponseRedirect(self.get_success_url())
    

    def get_success_url(self):
        pks = ','.join(map(str, self.updated))
        return reverse("uploaded_tracks") + f'?albums={pks}'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs


class UploadedTracksListView(LoginRequiredMixin, ListView):
    """
    View for uploaded tracks. Get the updates from the URL.
    """
    model = Album
    template_name = "testpages/uploaded_tracks.html"
    context_object_name = "albums"
    
    def get_queryset(self):
        pks = self.request.GET.get('albums', '')
        if not pks:
            return None
        return Album.objects.filter(pk__in=pks.split(','))


class ProfileAlbumsListView(LoginRequiredMixin, ListView):
    """
    Browse all the albums you've uploaded to the site.
    """
    model = Album
    template_name = "testpages/my_albums.html"
    context_object_name = "albums"
    
    def get_queryset(self):
        user = self.request.user.django_user
        return Album.objects.filter(uploader=user)\
                            .select_related('artist')\
                            .prefetch_related('tracks')


class ProfileArtistsListView(LoginRequiredMixin, ListView):
    """
    Browse all your artists uploaded to the site
    """
    model = Artist
    template_name = "testpages/my_artists.html"
    context_object_name = "artists"
    
    def get_queryset(self):
        user = self.request.user.django_user
        qs = Artist.objects.filter(album__uploader=user).distinct().prefetch_related('album_set')
        artist_list = list(qs)
        for artist in artist_list:
            first_album = artist.album_set.first()
            artist.icon_url = first_album.cover if first_album else None
            
        return artist_list


class ProfileSingleAlbumDetailView(LoginRequiredMixin, DetailView):
    """
    View for a single album. Uses a single django partial.
    """
    model = Album
    template_name = "testpages/album.html"
    context_object_name = "album"


class ProfileSingleArtistDetailView(LoginRequiredMixin, DetailView):
    """
    Display a single artist, with their albums.
    """
    model = Artist
    template_name = "testpages/artist.html"
    context_object_name = "artist"

    def get_queryset(self):
        return Artist.objects.all().prefetch_related('album_set')
    

class DeleteAlbumView(LoginRequiredMixin, DeleteView):
    """
    Delete a single album.
    """
    model = Album
    template_name = "testpages/delete_album.html"
    context_object_name = "album"
    
    def get_object(self):
        pk = self.kwargs["pk"]
        user = self.request.user.django_user
        album = get_object_or_404(Album, pk=pk, uploader=user)
        return album

    def get_success_url(self):
        return reverse('my_albums')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Single profile view.
    """
    model = Profile
    template_name = "testpages/profile.html"
    context_object_name = "profile"
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update profile view.
    """
    model = Profile
    form_class          = UpdateProfileForm
    template_name       = "testpages/update_profile_form.html"
    context_object_name = "profile"
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


def search_view(request):
    """
    Build the search results using django's Q, with
    icontains on album names and artist names.
    """
    query = request.GET.get('q', '')
    album_results = []
    artist_results = []

    if query:

        album_results = Album.objects.filter(
            Q(name__icontains=query) & (Q(is_private=False) | Q(uploader__isnull=True))
        ).distinct()
        
        artist_results = Artist.objects.filter(name__icontains=query).distinct()

    context = {
        'query': query,
        'album_results': album_results,
        'artist_results': artist_results,
    }
    return render(request, 'testpages/search_results.html', context)

#
# Unused for dev pages
# To preview css
#

def grid(request: HttpRequest):
    return render(request, "testpages/grid.html", context)

def grid_scrollable(request : HttpRequest):
    return render(request, "testpages/grid_scrollable.html", context)
