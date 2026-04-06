# urls.py
# Theodore Harlan
# hpt@bu.edu
# Friday April 3rd
# Description: url patterns for the Views in dad joke api



from django.urls import path
from . import views

urlpatterns = [
    path("", views.random_joke, name="random"),
    path("joke/<int:pk>", views.joke, name="joke"),
    path("jokes/", views.jokes, name="joke"),
    path("pictures", views.pictures, name="pictures"),
    path("picture/<int:pk>", views.picture, name="picture"),
    
    path('api/', views.api_random_joke, name='api_root'),
    path('api/random', views.api_random_joke, name='api_random_joke'),
    path('api/jokes', views.api_jokes, name='api_jokes'),
    path('api/joke/<int:pk>', views.api_joke, name='api_joke_detail'),
    path('api/pictures', views.api_pictures, name='api_pictures'),
    path('api/picture/<int:pk>', views.api_picture, name='api_picture_detail'),
    path('api/random_picture', views.api_random_picture, name='api_random_picture'),
]


# '' - show one Joke and one Picture selected at random
# 'random' - show one Joke and one Picture selected at random
# 'jokes' - show a page with all Jokes (no images)
# 'joke/<int:pk>' - show one Joke by its primary key
# 'pictures' - show a page with all Pictures (no jokes)
# 'picture/<int:pk>' - show one Picture by its primary key