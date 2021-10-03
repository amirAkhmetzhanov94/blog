from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, FormView, ListView
from webapp.models import Type, Status, Issue
from webapp.forms import IssueForm
from django.urls import reverse


class IndexView(ListView):
    model = Issue
    template_name = 'index.html'
    context_object_name = 'issues'
    ordering = "-update_time"
    paginate_by = 10


class IssueView(TemplateView):
    template_name = 'issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['issue_pk'])
        return context


class AddIssue(FormView):
    template_name = 'issue_create.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("issue_detail", kwargs={"issue_pk": self.issue.pk})


class UpdateIssue(FormView):
    template_name = "issue_update.html"
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Issue, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issue"] = self.issue
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.issue
        return kwargs

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("issue_detail", kwargs={"issue_pk": self.issue.pk})


class DeleteIssue(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        return render(request, 'issue_delete.html', context={'issue': issue})

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect('index')
