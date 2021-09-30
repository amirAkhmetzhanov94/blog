from django import forms
from django.forms import widgets
from webapp.models import Issue

special_attributes = {"class": "form-control"}


class IssueForm(forms.ModelForm):
    class Meta:
        exclude = ["creation_time", "update_time"]
        model = Issue
