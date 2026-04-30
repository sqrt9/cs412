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
from .models import *
from .forms import *
from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import redirect


# Create your views here.

context = {}

def base(request : HttpRequest):
    context = {}
    if request.user.username:
        profile_url = reverse('profile', kwargs={'username': request.user.username})
        context["profile_url"] = profile_url
    return render(request, template_name="testpages/links.html", context=context)

def grid(request: HttpRequest):
    return render(request, "testpages/grid.html", context)

def grid_scrollable(request : HttpRequest):
    return render(request, "testpages/grid_scrollable.html", context)

class CreateAccountView(CreateView):
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
        
        
        update_albums, update_artists = set()
        track_list = []
        
        for f in files:
            track = Track.objects.create(track_file=f)
            updated_album, updated_artist = track.populate(user=self.request.user.django_user,
                                                           private=is_private,
                                                           from_file=from_file,
                                                           search=search)
            if search:
                update_albums.add(updated_album)
                update_artists.add(updated_artist)
                track_list.append(track.track_title)
        
        if search:
            # number, disk number, album, artists and cover
            # are unset if returning from populate using only search
            # at this point. 

        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        pks = ','.join(map(str, self.updated))
        return reverse("uploaded_tracks") + f'?albums={pks}'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs


class UploadedTracksListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = "testpages/uploaded_tracks.html"
    context_object_name = "albums"
    
    def get_queryset(self):
        pks = self.request.GET.get('albums', '')
        if not pks:
            return None
        return Album.objects.filter(pk__in=pks.split(','))


class ProfileAlbumsListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = "testpages/my_albums.html"
    context_object_name = "albums"
    
    def get_queryset(self):
        user = self.request.user.django_user
        return Album.objects.filter(uploader=user)


class ProfileArtistsListView(LoginRequiredMixin, ListView):
    model = Artist
    template_name = "testpages/my_artists.html"
    context_object_name = "artists"
    
    def get_queryset(self):
        user = self.request.user.django_user
        return Artist.objects.filter(album__uploader=user).distinct()


class ProfileSingleAlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = "testpages/album.html"
    context_object_name = "album"


class ProfileSingleArtistDetailView(LoginRequiredMixin, DetailView):
    model = Artist
    template_name = "testpages/artist.html"
    context_object_name = "artist"
    
class DeleteAlbumView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = "testpages/delete_album.html"
    context_object_name = "album"
    
    def get_object(self):
        pk = self.kwargs["pk"]
        user = self.request.user.django_user
        album = get_object_or_404(Album, pk=pk, uploader=user)
        return album


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "testpages/profile.html"
    context_object_name = "profile"
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class          = UpdateProfileForm
    template_name       = "testpages/update_profile_form.html"
    context_object_name = "profile"
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user.django_user)

    def get_success_url(self):
        return reverse('profile',
                kwargs={
                    'username': self.request.user.django_user.username
                    }
                )

