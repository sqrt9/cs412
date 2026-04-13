# views.py
# Theodore Harlan
# hpt@bu.edu
# Created April 2
# DESCRIPTION:
# ---
# Views for dad joke pages
# ---


from django.shortcuts import render
from .models import *
import random
from django.http import JsonResponse
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer

# Create your views here.


def jokes(request):
    return render(request, 'dadjokes/jokes.html', {'jokes': Joke.objects.all()})

def joke(request, pk):
    joke = Joke.objects.get(pk=pk)
    return render(request, 'dadjokes/joke.html', {'joke': joke, 'picture': picture})

def pictures(request):
    return render(request, 'dadjokes/pictures.html', {'pictures': Picture.objects.all()})

def picture(request, pk):
    picture = Picture.objects.get(pk=pk)
    return render(request, 'dadjokes/picture.html', {'picture': picture})

def random_joke(request):
    all_jokes = Joke.objects.all()
    all_pics = Picture.objects.all()
    
    j = random.choice(all_jokes) 
    p = random.choice(all_pics)
    
    return render(request, 'dadjokes/joke.html', {'joke': j, 'picture': p})


def api_random_joke(request):
    jokes = Joke.objects.all()
    joke = random.choice(jokes)
    serializer = JokeSerializer(joke)
    return JsonResponse(serializer.data)

def api_jokes(request):
    if request.method == 'GET':
        jokes = Joke.objects.all()
        serializer = JokeSerializer(jokes, many=True)
        return JsonResponse(serializer.data, safe=False) # safe=False is needed for lists
    
    elif request.method == 'POST':
        import json
        data = json.loads(request.body)
        serializer = JokeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def api_joke(request, pk):
    joke = Joke.objects.get(pk=pk)
    return JsonResponse(JokeSerializer(joke).data)

def api_pictures(request):
    pics = Picture.objects.all()
    serializer = PictureSerializer(pics, many=True)
    return JsonResponse(serializer.data, safe=False)

def api_picture(request, pk):
    pic = Picture.objects.get(pk=pk)
    return JsonResponse(PictureSerializer(pic).data)

def api_random_picture(request):
    pics = Picture.objects.all()
    pic = random.choice(pics)
    return JsonResponse(PictureSerializer(pic).data)