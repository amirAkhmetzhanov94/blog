from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Type, Status, Issue
from webapp.forms import IssueForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        extra_context = {'issues': Issue.objects.all()}
        return extra_context


class IssueView(TemplateView):
    template_name = 'issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=kwargs['issue_pk'])
        return context


class AddIssue(View):
    template_name = 'issue_create.html'
    form_class = IssueForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            issue = Issue.objects.create(
                summary=form.cleaned_data["summary"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                type=form.cleaned_data["type"]
            )
            return redirect('issue_detail', issue_pk=issue.pk)
        else:
            return render(request, 'issue_create.html', {"form": form})


class UpdateIssue(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        form = IssueForm(initial={
            'summary': issue.summary,
            'description': issue.description,
            'status': issue.status,
            'type': issue.type,
        })
        return render(request, "issue_update.html", context={"form": form,
                                                             "issue": issue})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        if form.is_valid():
            issue.summary = form.cleaned_data["summary"]
            issue.description = form.cleaned_data["description"]
            issue.status = form.cleaned_data["status"]
            issue.type = form.cleaned_data["type"]
            issue.save()
            return redirect('issue_detail', issue_pk=issue.pk)
        else:
            return render(request, 'issue_update.html', context={'form': form,
                                                                 'issue': issue})


class DeleteIssue(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        return render(request, 'issue_delete.html', context={'issue': issue})

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        issue.delete()
        return redirect('index')
