# views.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12
# Modified Feb. 20
# DESCRIPTION:
# ---
# Mini_insta app views, forms, etc. for manipulating
# viewing, editting and deleting models on the page. 
# ---

from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.db.models import Q

# Create your views here.
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from .models import Profile
from .models import Post
from .models import Photo


class SearchView(ListView):
    """
    Search on behalf of a user for Profiles and
    Posts matching a text query. Search Profile bios,
    Post captions, display and usernames for a non-case
    sensitive term. Build a queryset off that and redir
    to the results page if this view is called with a query.
    """
    
    template_name       = "mini_insta/search_results.html"
    context_object_name = "results"
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        """
        Check if it's a GET or POST, and decide whether to show
        search results or the search page
        """
        self.profile = Profile.objects.get(pk=self.kwargs['pk'])
        
        if 'query' not in self.request.GET:
            return render(request, 'mini_insta/search.html',
                          {'profile': self.profile}
                          )
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Check if this request has a search term,
        if so, run the query and display the set instead.
        """
        query = self.request.GET.get('query')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        """
        
        """
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        
        context['profile']  = self.profile
        context['query']    = query
        context['profiles'] = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) | 
            Q(bio__icontains=query)).distinct()
        
        return context
    

class PostFeedListView(ListView):
    """
    Detail view for feed-specific posts.
    """
    template_name       = "mini_insta/show_feed.html"
    context_object_name = "feed_posts"

    def get_queryset(self):
        # Call the main queryset creator for feeds for this profile
        self.profile = Profile.objects.get(pk=self.kwargs['pk'])
        return self.profile.get_feed_posts

    def get_context_data(self, **kwargs):
        # Finally tell the template renderer what profile this is
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

class ShowFollowersDetailView(DetailView):
    """
    View to show the followers of a profile.
    """
    model               = Profile
    context_object_name = "profile"
    template_name       = "mini_insta/followers.html"

class ShowFollowingDetailView(DetailView):
    """
    View to show what other profiles this profile is following.
    """
    model               = Profile
    context_object_name = "profile"
    template_name       = "mini_insta/following.html"


class DeletePostView(DeleteView):
    """
    Deletion page for a user post.
    """
    model               = Post
    context_object_name = "post"
    template_name       = "mini_insta/delete_post.html"
    
    def get_context_data(self, **kwargs):
        # Tell template renderer of this profile
        context            = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context
    
    def get_success_url(self):
        # Use reverse to go back to the profile after deletion
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateProfileForm(ModelForm):
    """
    Form view for updating some profile information for a user.
    """
    class Meta:
        # Info in this form, model and fields
        model  = Profile
        fields = ["display_name", "icon", "bio"]

class UpdateProfileView(UpdateView):
    """
    View in which to update profile information from.
    """
    model               = Profile
    form_class          = UpdateProfileForm
    template_name       = "mini_insta/update_profile_form.html"
    context_object_name = "profile"

class ProfileListView(ListView):
    """
    View for homepage, lists all profiles
    """
    model               = Profile
    template_name       = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """
    DetailView for profile page
    """
    model               = Profile
    template_name       = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    """
    DetailView for post page
    """
    model               = Post
    template_name       = "mini_insta/post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    """
    CreateView for create_post page
    get_context_data method when the template created
    form_valid method to INSERT the Post and Photo models
    """
    model         = Post
    template_name = "mini_insta/create_post_form.html"
    fields        = ["caption"]
    
    def get_context_data(self, **kwargs):
        # Tell template of this profile
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        return context
    
    def form_valid(self, form):
        # Save post to DB and optional Photo models included 
        profile      = Profile.objects.get(pk=self.kwargs["pk"])
        post         = form.save(commit=False)
        post.profile = profile
        post.save()

        media = self.request.FILES.getlist("media")
        for file in media:
            Photo.objects.create(media=file, post=post)

        self.object = post
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect on valid form to this post after .save()
        return reverse("show_post", kwargs={"pk": self.object.pk})