from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from .models import *

# Create your views here.

context = {}

def base(request : HttpRequest):
    return render(request, template_name="testpages/base.html", context=context)

def grid(request: HttpRequest):
    return render(request, "testpages/grid.html", context)

def grid_scrollable(request : HttpRequest):
    return render(request, "testpages/grid_scrollable.html", context)

class CreateCollectionArtistView(CreateView):
    model = CollectionArtist
    template_name = "testpages/create_artist.html"
    fields = ["collectionArtistName",
              "collectionArtistLocation",
              "collectionArtistDescription"]