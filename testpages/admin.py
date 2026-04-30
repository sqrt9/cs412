from django.contrib import admin
from .models import *
from django.apps import apps

# Register all models in the app
for model in apps.get_app_config('testpages').get_models():
    admin.site.register(model)