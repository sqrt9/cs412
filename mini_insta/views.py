from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Profile

class ProfileListView(ListView):
    model = Profile
    template_name = "show_all_profiles.html"
    context_object_name = "profiles"