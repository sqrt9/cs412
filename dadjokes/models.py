from django.db import models
from django.utils import timezone

# Create your models here.

class Joke(models.Model):
    """Joke model"""
    content     = models.TextField(default="")
    contributor = models.TextField(default="")
    timestamp   = models.DateField(default=timezone.now)

class Picture(models.Model):
    """picture model"""
    media     = models.URLField(default="")
    timestamp = models.DateField(default=timezone.now)
    

def load_jokes():
    Joke.objects.all().delete()
    Picture.objects.all().delete()
    author = "Linux Fortunes"
    jokes = [
        """Q:	Why did the tachyon cross the road?
A:	Because it was on the other side.""",
"""If God hadn't wanted you to be paranoid, He wouldn't have given you such a vivid imagination.""",
"""If the automobile had followed the same development as the computer, a Rolls-Royce would today cost $100, get a million miles per per gallon, and explode once a year killing everyone inside.
		-- Robert Cringely, InfoWorld""",
"""I have discovered the art of deceiving diplomats. I tell them the truth and they never believe me.
		-- Camillo Di Cavour""",
"""For thirty years a certain man went to spend every evening with Mme. ___.When his wife died his friends believed he would marry her, and urgedhim to do so.  "No, no," he said: "if I did, where should I have tospend my evenings?"
		-- Chamfort"""]
    images = ["https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c2021fe4-8d0a-409c-a5a7-3cece772fe03/dlbenab-313ea58a-d8c3-417a-b196-2f3309a9de2c.png/v1/fit/w_828,h_1196/mlp_pinkie_x_cadance_closed__by_littsandy_dlbenab-414w-2x.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTg1MCIsInBhdGgiOiIvZi9jMjAyMWZlNC04ZDBhLTQwOWMtYTVhNy0zY2VjZTc3MmZlMDMvZGxiZW5hYi0zMTNlYTU4YS1kOGMzLTQxN2EtYjE5Ni0yZjMzMDlhOWRlMmMucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.-4HQBrWxHGcDj3FRRHxdUKJKlGKuAaUyM075oxrDAsU",
              "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c2021fe4-8d0a-409c-a5a7-3cece772fe03/dlbhbz6-a7ecd886-59cf-48d9-9c81-aa22bdc4fe21.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiIvZi9jMjAyMWZlNC04ZDBhLTQwOWMtYTVhNy0zY2VjZTc3MmZlMDMvZGxiaGJ6Ni1hN2VjZDg4Ni01OWNmLTQ4ZDktOWM4MS1hYTIyYmRjNGZlMjEucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.2mQtBnch_Idg92GUvsn0ixJ-EH6oscyPudUfg4PZv0s",
              "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c2021fe4-8d0a-409c-a5a7-3cece772fe03/dlgw7vy-6723de0c-99bd-4769-af15-5c292a59cf47.png/v1/fit/w_828,h_986/mlp_custom_for_ashertales__1_by_littsandy_dlgw7vy-414w-2x.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTMwOCIsInBhdGgiOiIvZi9jMjAyMWZlNC04ZDBhLTQwOWMtYTVhNy0zY2VjZTc3MmZlMDMvZGxndzd2eS02NzIzZGUwYy05OWJkLTQ3NjktYWYxNS01YzI5MmE1OWNmNDcucG5nIiwid2lkdGgiOiI8PTEwOTkifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.sk-X-6G1J3nYpdW_7XgnkEN9xZK9SOJLcXVzd_1CCiI",
              "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c2021fe4-8d0a-409c-a5a7-3cece772fe03/dlhzgj3-90d3d621-3746-4f7a-813f-c1e65e6ecbc6.png/v1/fit/w_828,h_1094/mlp_custom_for_ashertales__5_by_littsandy_dlhzgj3-414w-2x.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTY5MCIsInBhdGgiOiIvZi9jMjAyMWZlNC04ZDBhLTQwOWMtYTVhNy0zY2VjZTc3MmZlMDMvZGxoemdqMy05MGQzZDYyMS0zNzQ2LTRmN2EtODEzZi1jMWU2NWU2ZWNiYzYucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ._WW9VgFYlky5cadxQDvHxuAe2yhDFJZQJU6zeyjKVMA",
              "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c2021fe4-8d0a-409c-a5a7-3cece772fe03/dlksdxz-809e6b2a-eca5-4740-bd87-594b6fde3106.png/v1/fill/w_911,h_877/mlp_raridash_closed_by_littsandy_dlksdxz-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTIzMyIsInBhdGgiOiIvZi9jMjAyMWZlNC04ZDBhLTQwOWMtYTVhNy0zY2VjZTc3MmZlMDMvZGxrc2R4ei04MDllNmIyYS1lY2E1LTQ3NDAtYmQ4Ny01OTRiNmZkZTMxMDYucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.WR7aVh6YYeP8wQG4NvaedULTXJWMLmSSDjngH2KotBc",
              "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c2021fe4-8d0a-409c-a5a7-3cece772fe03/dlf9uw1-41cdd25d-c2aa-4933-85b3-a01b1194f1f2.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiIvZi9jMjAyMWZlNC04ZDBhLTQwOWMtYTVhNy0zY2VjZTc3MmZlMDMvZGxmOXV3MS00MWNkZDI1ZC1jMmFhLTQ5MzMtODViMy1hMDFiMTE5NGYxZjIucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.cz4vn1CK1rFjdnxTa6NPUAdgDqvJcXEVQEJjYXCNb2Y",
              ]
    for joke in jokes:
        Joke.objects.create(content=joke, contributor=author) #Theyre all from the same source
    for picture in images:
        Picture.objects.create(media=picture)
    
    