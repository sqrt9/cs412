# views.py
# Theodore Harlan
# hpt@bu.edu
# Created Feb. 12

from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from .models import Profile
from .models import Post
from .models import Photo

class ProfileListView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    model = Post
    template_name = "mini_insta/create_post_form.html"
    fields = ["caption"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        return context
    
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        post = form.save(commit=False)
        post.profile = profile
        post.save()

        image_url = self.request.POST.get("image_url")
        if image_url:
            Photo.objects.create(loc=image_url, post=post)

        self.object = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show_post", kwargs={"pk": self.object.pk})