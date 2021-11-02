from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError

from accounts.models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.CharField(label="Email", required=True)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name == "" and last_name == "":
            raise ValidationError("First name or Last name is required")
        return cleaned_data

    class Meta(UserCreationForm.Meta):
        fields = ["username", "first_name",
                  "last_name", "email", "password1", "password2"]


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Name", "last_name": "Surname", "email": "Email"}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

