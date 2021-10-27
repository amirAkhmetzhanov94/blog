from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError


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
