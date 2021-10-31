from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DeleteView, CreateView, UpdateView
from webapp.models import Issue
from django.utils.http import urlencode
from webapp.forms import IssueForm, SearchForm
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin


class IndexView(ListView):
    model = Issue
    template_name = 'issues/index.html'
    context_object_name = 'issues'
    ordering = "-update_time"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["search_form"] = self.form
        if self.search_value:
            context["query"] = urlencode({"search": self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data["search"]


class AddIssue(PermissionRequiredMixin, CreateView):
    template_name = 'issues/create.html'
    form_class = IssueForm
    model = Issue
    permission_required = "webapp.add_issue"

    def get_success_url(self):
        print(self.object.project.pk)
        return reverse("webapp:index")

class IssueView(TemplateView):
    template_name = 'issues/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['issue_pk'])
        return context


class UpdateIssue(UserPassesTestMixin, UpdateView):
    template_name = "issues/update.html"
    form_class = IssueForm
    model = Issue

    def test_func(self):
        pk = self.kwargs.get("pk")
        issue = get_object_or_404(Issue, pk=pk)
        return self.request.user in issue.project.users.all() and self.request.user.has_perm("webapp.change_issue")

    def get_success_url(self):
        return reverse("webapp:project_detail", kwargs={"pk": self.object.project.pk})


class DeleteIssue(UserPassesTestMixin, DeleteView):
    template_name = 'issues/delete.html'
    form_class = IssueForm
    model = Issue
    context_object_name = 'issues'

    def test_func(self):
        pk = self.kwargs.get("pk")
        issue = get_object_or_404(Issue, pk=pk)
        return self.request.user in issue.project.users.all() and self.request.user.has_perm("webapp.delete_issue")

    def get_success_url(self):
        id = self.kwargs.get("pk")
        project = get_object_or_404(Issue, pk=id)
        return reverse('webapp:project_detail', kwargs={"pk": project.project.pk})
