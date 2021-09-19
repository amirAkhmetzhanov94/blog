from django import forms
from django.forms import widgets
from webapp.models import Type, Status

special_attributes = {"class": "form-control"}


class IssueForm(forms.Form):
    summary = forms.CharField(max_length=30, required=True, label='Summary',
                              widget=widgets.Input(attrs=special_attributes))
    description = forms.CharField(max_length=2000, label='Description',
                                  widget=widgets.Textarea(attrs=special_attributes))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Status",
                                    widget=widgets.Select(attrs=special_attributes))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label="Type",
                                          widget=widgets.SelectMultiple(attrs=special_attributes))
