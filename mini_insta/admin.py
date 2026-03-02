# admin.py
# Theodore Harlan
# hpt@bu.edu
# Auto generated
# Available models in the django admin console
# Modified Feb. 20

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)