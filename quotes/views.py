# File: views.py
# Created: Jan. 29
# Author: Theodore Harlan
#         hpt@bu.edu
# Description: quotes/ view handler

from django.shortcuts import render
import random

# Global array of quotes
quotes = [
    """
    The cradle rocks above an abyss, and common sense tells us that our existence is but a brief crack of light between two eternities of darkness. Although the two are identical twins, man, as a rule, views the prenatal abyss with more calm than the one he is heading for (at some forty-five hundred heartbeats an hour)
    
    --Nabokov, Speak, Memory
    
    """,
    """
    It’s always the idle habits you acquire which you will regret. Father said that. That Christ was not crucified: he was worn away by a minute clicking of little wheels.
    
    -- William Faulkner, The Sound and the Fury
    
    """,
    """
    The meek shall inherit the earth” meant nothing to me. The meek were battered in West Baltimore, stomped out at Walbrook Junction, bashed up on Park Heights, and raped in the showers of the city jail. My understanding of the universe was physical, and its moral arc bent toward chaos then concluded in a box.
    
    -- Ta-Nehisi Coates, Between the World and Me
    
    """
]

# Global array of images
images = [
    "https://pbs.twimg.com/media/G_6JezlaMAAibUm.jpg?name=orig",
    "https://pbs.twimg.com/media/G_6JezlbkAEd0rh.jpg?name=orig",
    "https://pbs.twimg.com/media/G6NXDfsaMAAFETw.jpg?name=orig"
]

# View: quote
def quote(request):
    """Return a render of a random quote and image from the view."""

    ri = random.randint(0,2)
    ru = random.randint(0,2)

    context = {"random_quote": quotes[ru],
               "random_image_url": images[ri]}

    return render(request, "quotes/quote.html", context)

# View: show_all
def show_all(request):
    """Show all 3 quotes and images in the view."""
    
    context = {
        "quote1" : quotes[0],
        "quote2" : quotes[1],
        "quote3" : quotes[2],
        "image1" : images[0],
        "image2" : images[1],
        "image3" : images[2]
        }
    
    return render(request, "quotes/show_all.html", context)

# View: about
def about(request):
    """Return an about page of the authors."""
    
    context = {
        "about" : "Hello"
        }
    
    return render(request, "quotes/about.html", context)
