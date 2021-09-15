from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Type, Status, Issue


class IndexView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        context = {'issues': issues}
        return render(request, 'index.html', context)
