from django.views.generic import ListView
from webapp.models import Project


class ProjectList(ListView):
    model = Project
    template_name = 'projects/index.html'

