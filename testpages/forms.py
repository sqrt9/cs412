from django import forms
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

class CreateAccountForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "display_name",
            "profile_description",
            "profile_icon"
        ]

class XUserCreationForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2'
                  ]


class UpdateProfileForm(LoginRequiredMixin, ModelForm):
    class Meta:
        model  = Profile
        fields = [
            "display_name",
            "profile_icon",
            "profile_description"
            ]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()
