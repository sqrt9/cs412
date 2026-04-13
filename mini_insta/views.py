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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


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


from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework          import status
from rest_framework.parsers  import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
 
from .serializers  import ProfileSerializer, PostSerializer, PostCreateSerializer

from rest_framework.permissions  import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token

from django.shortcuts            import get_object_or_404
from django.contrib.auth        import authenticate
 
TOKEN_AUTH  = [TokenAuthentication, SessionAuthentication]
PUBLIC_PERM = [IsAuthenticatedOrReadOnly]
AUTH_PERM   = [IsAuthenticated]
 
 
# ── Login / Logout ────────────────────────────────────────────────────────────
 
class LoginAPIView(APIView):
    """
    POST /api/login/
    { "username": "...", "password": "..." }
    → { "token": "...", "profile_id": 1, "username": "..." }
    """
    authentication_classes = []
    permission_classes     = []
 
    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")
 
        if not username or not password:
            return Response(
                {"detail": "username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
 
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
 
        token, _ = Token.objects.get_or_create(user=user)
 
        try:
            profile_id = user.profile.pk
        except Exception:
            profile_id = None
 
        return Response({
            "token":      token.key,
            "profile_id": profile_id,
            "username":   user.username,
        })
 
 
class LogoutAPIView(APIView):
    """
    POST /api/logout/
    Header: Authorization: Token <key>
    """
    authentication_classes = TOKEN_AUTH
    permission_classes     = AUTH_PERM
 
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out."})
 
 
# ── Profiles ──────────────────────────────────────────────────────────────────
 
class ProfileListAPIView(APIView):
    """GET /api/profiles/  — list all; ?search=<term> to filter"""
    authentication_classes = TOKEN_AUTH
    permission_classes     = PUBLIC_PERM
 
    def get(self, request):
        qs   = Profile.objects.all()
        term = request.query_params.get("search", "").strip()
        if term:
            from django.db.models import Q
            qs = qs.filter(
                Q(username__icontains=term) |
                Q(display_name__icontains=term) |
                Q(bio__icontains=term)
            ).distinct()
        return Response(ProfileSerializer(qs, many=True, context={"request": request}).data)
 
 
class ProfileDetailAPIView(APIView):
    """GET /api/profiles/<pk>/"""
    authentication_classes = TOKEN_AUTH
    permission_classes     = PUBLIC_PERM
 
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        return Response(ProfileSerializer(profile, context={"request": request}).data)
 
 
# ── Posts ─────────────────────────────────────────────────────────────────────
 
class ProfilePostsAPIView(APIView):
    """GET /api/profiles/<pk>/posts/"""
    authentication_classes = TOKEN_AUTH
    permission_classes     = PUBLIC_PERM
 
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        posts   = Post.objects.filter(profile=profile).order_by("-timestamp")
        return Response(PostSerializer(posts, many=True, context={"request": request}).data)
 
 
class ProfilePostCreateAPIView(APIView):
    """POST /api/profiles/<pk>/posts/create/  (multipart — caption + media files)"""
    authentication_classes = TOKEN_AUTH
    permission_classes     = AUTH_PERM
    parser_classes         = [MultiPartParser, FormParser, JSONParser]
 
    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
 
        if profile.user != request.user:
            return Response(
                {"detail": "You may only create posts for your own profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
 
        serializer = PostCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        post = serializer.save(profile=profile)
        for file in request.FILES.getlist("media"):
            Photo.objects.create(media=file, post=post)
 
        return Response(
            PostSerializer(post, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
 
 
# ── Feed ──────────────────────────────────────────────────────────────────────
 
class ProfileFeedAPIView(APIView):
    """GET /api/profiles/<pk>/feed/  — requires auth; must be own profile"""
    authentication_classes = TOKEN_AUTH
    permission_classes     = AUTH_PERM
 
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
 
        if profile.user != request.user:
            return Response(
                {"detail": "You may only view your own feed."},
                status=status.HTTP_403_FORBIDDEN,
            )
 
        posts = profile.get_feed_posts
        return Response(PostSerializer(posts, many=True, context={"request": request}).data)