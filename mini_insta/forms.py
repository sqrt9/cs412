# File: forms.py
# Author: Theodore Harlan
# hpt@bu.edu
# Created Mar 5
# Description
# ---
# All forms used in the mini_insta app

from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class UpdateProfileForm(LoginRequiredMixin, ModelForm):
    """
    Form view for updating some profile information for a user.
    """
    class Meta:
        # Info in this form, model and fields
        model  = Profile
        fields = ["display_name", "icon", "bio"]
        

class CreateProfileForm(ModelForm):
    """
    Small form for profile creation.
    """
    class Meta:
        model = Profile
        fields = ["username", "display_name", "bio", "icon"]