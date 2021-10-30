from django.views.generic import ListView, DetailView, CreateView, UpdateView
from webapp.models import Project, Issue
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from webapp.forms import IssueForm, ProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/index.html'


class ProjectDetailedView(DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issues"] = Issue.objects.filter(project=self.object.pk)
        project_users = self.get_object().users.all()
        context["project_users"] = project_users
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/create.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:project_list')


class ProjectCreateIssue(LoginRequiredMixin, CreateView):
    model = Issue
    template_name = "issues/create.html"
    fields = ["summary", "description", "status", "type"]

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=pk)
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=pk)
        return reverse("webapp:project_detail", kwargs={"pk": project.pk})