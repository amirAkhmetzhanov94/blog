from django.views.generic import ListView, DetailView, CreateView
from webapp.models import Project, Issue
from django.urls import reverse


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/index.html'


class ProjectDetailedView(DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issues"] = Issue.objects.filter(task=kwargs['object'].pk)
        return context
