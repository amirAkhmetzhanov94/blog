from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import Type, Status, Issue


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {'issues': Issue.objects.all()}