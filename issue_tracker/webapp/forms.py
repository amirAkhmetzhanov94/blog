from django import forms
from django.forms import widgets
from webapp.models import Issue, Status, Type, Project
from django.utils.translation import gettext_lazy as _

special_attributes = {"class": "form-control"}


class IssueForm(forms.ModelForm):
    summary = forms.CharField(widget=widgets.TextInput(attrs=special_attributes), label=_("IssueFormSummary"))
    description = forms.CharField(widget=widgets.Textarea(attrs=special_attributes), label=_("IssueFormDescription"))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label=_("IssueFormStatus"),
                                    widget=widgets.Select(attrs=special_attributes))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label=_("IssueFormType"),
                                          widget=widgets.SelectMultiple(attrs=special_attributes))
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label=_("IssueFormProject"),
                                     widget=widgets.Select(attrs=special_attributes))

    class Meta:
        exclude = ["creation_time", "update_time"]
        model = Issue


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(widget=widgets.DateInput(attrs={"type": "date",
                                                                 "class": "form-control"}),
                                 label=_("ProjectFormStartDate"))
    finish_date = forms.DateField(widget=widgets.DateInput(attrs={"type": "date",
                                                                 "class": "form-control"}),
                                  label=_("ProjectFormFinishDate"))
    project_name = forms.CharField(widget=widgets.TextInput(attrs=special_attributes), label=_("ProjectFormProjectName"))
    project_summary = forms.CharField(widget=widgets.Textarea(attrs=special_attributes),
                                      label=_("ProjectFormProjectSummary"))

    class Meta:
        exclude = ['users']
        model = Project


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")
