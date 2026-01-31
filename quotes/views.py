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
    The cradle rocks above an abyss, and common sense tells us that our
    existence is but a brief crack of light between two eternities of darkness.
    Although the two are identical twins, man, as a rule, views the prenatal
    abyss with more calm than the one he is heading for (at some forty-five
    hundred heartbeats an hour)
    
    --Nabokov, Speak, Memory
    
    """,
    """
    It’s always the idle habits you acquire which you will regret. Father said
    that. That Christ was not crucified: he was worn away by a minute clicking
    of little wheels.
    
    -- William Faulkner, The Sound and the Fury
    
    """,
    """
    The meek shall inherit the earth” meant nothing to me. The meek were battered
    in West Baltimore, stomped out at Walbrook Junction, bashed up on Park Heights,
    and raped in the showers of the city jail. My understanding of the universe was
    physical, and its moral arc bent toward chaos then concluded in a box.
    
    -- Ta-Nehisi Coates, Between the World and Me
    
    """,
]

# Global array of images
images = [
    "https://pbs.twimg.com/media/G_6JezlaMAAibUm.jpg?name=orig",
    "https://pbs.twimg.com/media/G_6JezlbkAEd0rh.jpg?name=orig",
    "https://pbs.twimg.com/media/G6NXDfsaMAAFETw.jpg?name=orig",
]


# View: quote
def quote(request):
    """Return a render of a random quote and image from the view."""

    ri = random.randint(0, 2)
    ru = random.randint(0, 2)

    context = {"random_quote": quotes[ru], "random_image_url": images[ri]}

    return render(request, "quotes/quote.html", context)


# View: show_all
def show_all(request):
    """Show all 3 quotes and images in the view."""

    context = {
        "quote1": quotes[0],
        "quote2": quotes[1],
        "quote3": quotes[2],
        "image1": images[0],
        "image2": images[1],
        "image3": images[2],
    }

    return render(request, "quotes/show_all.html", context)


# View: about
def about(request):
    """Return an about page of the authors."""

    context = {
        "about": """"Ta-Nehisi Paul Coates (pronounced TAH-nə-HAH-see; born September 30, 1975)
        is a progressive American author, journalist, and activist. He gained a wide readership 
        during his time as national correspondent at The Atlantic, where he wrote about cultural,
        social, and political issues, particularly regarding African Americans and white supremacy.

        Vladimir Vladimirovich Nabokov (Russian: Владимир Владимирович Набоков; 22 April
        [O.S. 10 April] 1899 – 2 July 1977), also known by the pen name Vladimir Sirin,
        was a Russian and American novelist, poet, translator, and entomologist.
        Born in Imperial Russia in 1899, Nabokov wrote his first nine novels in Russian
        (1926–1938) while living in Berlin, where he met his wife, Véra Nabokov. He achieved
        international acclaim and prominence after moving to the United States, where he began
        writing in English. Trilingual in Russian, English, and French, Nabokov became a U.S.
        citizen in 1945 and lived mostly on the East Coast before returning to Europe in 1961,
        where he settled in Montreux, Switzerland.

        William Cuthbert Faulkner (pronounced FOCK-ner; September 25, 1897 – July 6, 1962) was an
        American writer. He is best known for his novels and short stories set in the fictional
        Yoknapatawpha County, Mississippi, a stand-in for Lafayette County where he spent most of
        his life. Winner of the 1949 Nobel Prize in Literature, Faulkner is one of the most celebrated
        writers of American literature, often considered the greatest writer of Southern literature
        and regarded as one of the most influential and important writers of the 20th century."
        """
    }

    return render(request, "quotes/about.html", context)
