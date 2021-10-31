from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Project, Issue
from django.urls import reverse
from django.shortcuts import get_object_or_404
from webapp.forms import ProjectForm
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin


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


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/create.html'
    form_class = ProjectForm
    permission_required = "webapp.add_project"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:project_list')


class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'projects/delete.html'
    model = Project
    context_object_name = 'project'

    def test_func(self):
        return self.request.user.has_perm("webapp.delete_project")

    def get_success_url(self):
        return reverse("webapp:project_list")


class ProjectUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'projects/update.html'
    model = Project
    context_object_name = 'project'
    form_class = ProjectForm

    def test_func(self):
        return self.request.user.has_perm("webapp.change_project")

    def get_success_url(self):
        return reverse("webapp:project_detail", kwargs={"pk": self.object.pk})


class ProjectCreateIssue(UserPassesTestMixin, CreateView):
    model = Issue
    template_name = "issues/create.html"
    fields = ["summary", "description", "status", "type"]

    def test_func(self):
        pk = self.kwargs.get("pk")
        project = get_object_or_404(Project, pk=pk)
        return self.request.user in project.users.all() and self.request.user.has_perm("webapp.add_issue")

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
