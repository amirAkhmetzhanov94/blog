from django import forms
from django.forms import widgets
from webapp.models import Issue, Status, Type

special_attributes = {"class": "form-control"}


class IssueForm(forms.ModelForm):
    summary = forms.CharField(widget=widgets.TextInput(attrs=special_attributes))
    description = forms.CharField(widget=widgets.Textarea(attrs=special_attributes))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Status",
                                    widget=widgets.Select(attrs=special_attributes))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label="Type",
                                          widget=widgets.SelectMultiple(attrs=special_attributes))

    class Meta:
        exclude = ["creation_time", "update_time"]
        model = Issue


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")
