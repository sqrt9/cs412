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
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.views.generic import View
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile, Post, Photo, Follow, Like
from .forms import *

class CreateProfileView(CreateView):
    """
    View for profile creation page. Displays and submits two forms:
    one for the django User (from Usercreation), and one to
    build out the Profile model from.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(
            self.request,
            user,
            backend="django.contrib.auth.backends.ModelBackend"
        )
        form.instance.user = user
        return super().form_valid(form)
    

class MyProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        return redirect("show_profile", pk=profile.pk)


class SearchView(LoginRequiredMixin, ListView):
    """
    Search on behalf of a user for Profiles and
    Posts matching a text query. Search Profile bios,
    Post captions, display and usernames for a non-case
    sensitive term. Build a queryset off that and redir
    to the results page if this view is called with a query.
    """
    template_name       = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """
        Check if it's a GET or POST, and decide whether to show
        search results or the search page.
        """
        # use the logged‑in profile now instead of a URL pk
        self.profile = request.user.profile

        # if no query string, show the search form
        if 'query' not in request.GET:
            return render(request, 'mini_insta/search.html',
                          {'profile': self.profile}
                          )

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Check if this request has a search term,
        if so, run the query and display the set instead.
        """
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        """
        Add back profile and other search context.
        """
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')

        context['profile']  = self.profile
        context['query']    = query
        context['profiles'] = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) | 
            Q(bio__icontains=query)).distinct()

        return context
    

class PostFeedListView(LoginRequiredMixin, ListView):
    """
    Detail view for feed-specific posts.
    """
    template_name       = "mini_insta/show_feed.html"
    context_object_name = "feed_posts"
    
    def get_queryset(self):
        self.profile = Profile.objects.get(pk=self.request.user.profile.pk)
        return self.profile.get_feed_posts

    def get_context_data(self, **kwargs):
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


class DeletePostView(LoginRequiredMixin, DeleteView):
    """
    Deletion page for a user post.
    """
    model               = Post
    context_object_name = "post"
    template_name       = "mini_insta/delete_post.html"
    
    def get_queryset(self):
        return Post.objects.filter(profile=self.request.user.profile)
    
    def get_context_data(self, **kwargs):
        # Tell template renderer of this profile
        context = super().get_context_data(**kwargs)
        context["post"] = self.object
        return context
    
    def get_success_url(self):
        # Use reverse to go back to the profile after deletion
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})



class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View in which to update profile information from.
    """
    model               = Profile
    form_class          = UpdateProfileForm
    template_name       = "mini_insta/update_profile_form.html"
    context_object_name = "profile"
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self):
        return f"/mini_insta/profile/{self.request.user.profile.pk}/"


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

class CreatePostView(LoginRequiredMixin, CreateView):
    """
    CreateView for create_post page
    get_context_data method when the template created
    form_valid method to INSERT the Post and Photo models
    """
    model = Post
    template_name = "mini_insta/create_post_form.html"
    fields = ["caption"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile
        return context

    def form_valid(self, form):
        profile = self.request.user.profile

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        media = self.request.FILES.getlist("media")
        for file in media:
            Photo.objects.create(media=file, post=post)

        self.object = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show_post", kwargs={"pk": self.object.pk})
    

class FollowView(LoginRequiredMixin, TemplateView):
    """Create a follow relationship"""
    def dispatch(self, request, *args, **kwargs):
        followee = Profile.objects.get(pk=self.kwargs["pk"])
        follower = Profile.objects.get(user=request.user)

        if follower != followee:
            Follow.objects.get_or_create(
                follower=followee,
                followee=follower,
                defaults={"timestamp": timezone.now()}
            )
        return redirect("show_profile", pk=followee.pk)
    
    
class DeleteFollowView(LoginRequiredMixin, TemplateView):
    """Delete a follow relationship"""
    def dispatch(self, request, *args, **kwargs):
        followee = Profile.objects.get(pk=self.kwargs["pk"])
        follower = Profile.objects.get(user=request.user)
        Follow.objects.filter(
            follower=follower,
            followee=followee
        ).delete()
        return redirect("show_profile", pk=followee.pk)
    
class LikeView(LoginRequiredMixin, TemplateView):
    """Like a post"""
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=request.user)
        Like.objects.get_or_create(
            post=post,
            profile=profile,
            defaults={"timestamp": timezone.now()}
        )
        return redirect("show_post", pk=post.pk)
    
class DeleteLikeView(LoginRequiredMixin, TemplateView):
    """Unlike a post"""
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=request.user)
        Like.objects.filter(
            post=post,
            profile=profile
        ).delete()
        return redirect("show_post", pk=post.pk)

from rest_framework import generics
from .serializers import ProfileSerializer
from .serializers import PostSerializer
from .serializers import PostCreateSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

class ProfileListAPIView(generics.ListAPIView):
    """Return a serialized list of profiles"""
    queryset           = Profile.objects.all()
    serializer_class   = ProfileSerializer
    permission_classes = [AllowAny]             # allow everyone to view all profiles
    
class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    """Return a single profile, serialized"""
    queryset = Profile.objects.all() # RetrieveAPIView will internally filter
                                     # this with it's get_object() method
    serializer_class   = ProfileSerializer
    permission_classes = [AllowAny]         # All profiles are public

class ProfilePostsListAPIView(generics.ListAPIView):
    """Return a list of posts from a profile"""
    serializer_class   = PostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):         # Because it's not a RetrieveView,
        pk = self.kwargs['pk']      # it needs a get_queryset method
        return Post.objects.filter(profile__pk=pk)
    
class ProfilePostCreateAPIView(generics.CreateAPIView):
    """API create a post from a caption"""
    serializer_class   = PostCreateSerializer  # Need a different serializer
                                               # because posts are only made
    permission_classes = [IsAuthenticated]     # via caption, so the fields
                                               # must be different than PostSerializer
    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)

class ProfileFeedListAPIView(generics.ListAPIView):
    """Return a feed of posts for a profile"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]    # Only the logged-in user cans 
                                              # see their own feeds
    def get_queryset(self):
        profile = self.request.user.profile
        return profile.get_feed_posts